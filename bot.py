from util.config import authenticate
from streamer import MoeListener
from run_generator import Generator
import tweepy

## TODO we're gonna scrap streaming in tweepy because it seems pretty dead
## Set up webhook and integrate w/ Account Activity API
## Set up some simple web app to handle the webhook stuff
## Webapp places valid events (mentions, dm's) into a queue or something like that
## This app streams events from the queue and handles them, replying if needed.
class Moetron:

    def __init__(self, api):
        self.api = api
        generator = Generator()
        self.moeListener = MoeListener(api, generator)
        self.moeStream = tweepy.Stream(auth = api.auth, listener=self.moeListener)
    
        

    # Stream handler, sadly since a lot of streaming was deprecated it only works for replies...
    def listen_stream(self):
        self.moeStream.filter(follow=['1359290611988316161'])

def runBot():
    moetron = Moetron(authenticate())
    moetron.listen_stream()


if __name__ == '__main__':
    runBot()