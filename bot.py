from util.config import authenticate
from handler import MoeHandler
from run_generator import Generator
import tweepy
import os

MOEQUE_CONN_STRING = os.environ.get('MOEQUE_CONN_STRING')
QUEUE_NAME = os.environ.get('QUEUE_NAME')

class Moetron:

    def __init__(self, api):
        self.api = api
        generator = Generator()
        self.moeHandler = MoeHandler(api, generator, QUEUE_NAME, MOEQUE_CONN_STRING)

    def handle_events(self):
        self.moeHandler.read_messages()

def runBot():
    moetron = Moetron(authenticate())
    moetron.handle_events()


if __name__ == '__main__':
    runBot()