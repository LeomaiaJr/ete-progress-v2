import tweepy
from tweepy import TweepError

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
TOKEN = ""
SECRET_TOKEN = ""


class TwitterProvider:
    def __init__(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(TOKEN, SECRET_TOKEN)

        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                              wait_on_rate_limit_notify=True)
        self.check_status()

    def check_status(self):
        try:
            self.api.verify_credentials()
            print("Authentication OK")
        except TweepError as e:
            raise TweepError(f"Error during authentication. Details: {e}")

    def tweet_sth(self, text):
        self.api.update_status(text)
