import tweepy
from generate import Generate_util
import json


# The gut of moetron, this listens to mentions / replies to moetron and triggers the generation of images
class MoeListener(tweepy.StreamListener):

    def __init__(self, api, generator):
        super()
        self.api = api
        self.gen_util = Generate_util(generator)

    # Handle incoming mentions, replies.
    # Apparently streaming for DMs is dead
    def on_data(self, inc_data):
        try:
            data = json.loads(inc_data)
            if 'in_reply_to_user_id' in data and data['in_reply_to_user_id'] == 1359290611988316161:
                imgpth = self.gen_util.parse_msg(data['text'])
                self.api.update_with_media(imgpth, status="Here's your generated anime girl!", in_reply_to_status_id = data['id'], auto_populate_reply_metadata=True)
        except Exception as e:
            print("something went wrong")
            print(e)
            print('data: ',inc_data)
        return True

    def on_error(self, status_code):
        print("error")
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return False