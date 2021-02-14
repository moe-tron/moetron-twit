import tweepy
from generate import Generate_util
import json
import time
from azure.storage.queue import (
    QueueService,
    QueueMessageFormat)


# The gut of moetron, reads events from a queue, calls the generator to generate the images, and then responds to the event.
class MoeHandler():

    def __init__(self, api, generator, queue_name, conn_str):
        self.api = api
        self.gen_util = Generate_util(generator)
        self.queue_name = queue_name
        self.queue_service = QueueService(connection_string=conn_str)
        self.queue_service.create_queue(queue_name)

    # loops forever, reading messages and sending to gen util for parsing. Then sends the message
    def read_messages(self):
        while 1:
            try:
                messages = self.queue_service.get_messages(self.queue_name)
                if not messages:
                    time.sleep(2)  # We'll wait a few seconds and check again.
                    continue
                for message in messages:
                    event = json.loads(message.content)
                    if event['msg_type'] == 'tweet':
                        self.handle_tweet(event)
                    elif event['msg_type'] == 'dm':
                        self.handle_dm(event)
                    self.queue_service.delete_message(
                        self.queue_name, message.id, message.pop_receipt)
            except Exception as e:
                print("Exception handling messages")
                print(e)

    def handle_dm(self, event):
        imgpth = self.gen_util.parse_msg(event['text'])
        media = self.api.media_upload(imgpth)
        self.api.send_direct_message(
            recipient_id=event['user_id'], text="Here's your generated anime girl!", attachment_type='media', attachment_media_id=media.media_id)
        return

    def handle_tweet(self, event):
        imgpth = self.gen_util.parse_msg(event['text'])
        self.api.update_with_media(imgpth, status="Here's your generated anime girl!",
                                   in_reply_to_status_id=event['respond_id'], auto_populate_reply_metadata=True)
        return
