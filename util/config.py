import tweepy
import os

def authenticate():
    consumer_key = os.environ.get("TW_MOE_KEY")
    consumer_secret = os.environ.get("TW_MOE_SECRET")
    access_token = os.environ.get("TW_TOKEN")
    access_token_secret = os.environ.get("TW_TOKEN_SECRET")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        print("Error creating API")
        raise e
    print("API created")
    return api