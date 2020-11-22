from tweepy import StreamListener, API, OAuthHandler, Stream
import os
from dotenv import load_dotenv
from twitter.twitter_data import TwitterClient
import logging
load_dotenv()


xyz = TwitterClient('@chopra__mudit')
xyz.set_query(input('Enter the word you want to search'))
tweets = xyz.get_tweets()


logger = logging.getLogger()

def create_app():
    auth = OAuthHandler(
        os.getenv('CONSUMER_KEY'),
        os.getenv('CONSUMER_SECRET')
    )
    auth.set_access_token(
        os.getenv('ACCESS_TOKEN'),
        os.getenv('ACCESS_TOKEN_SECRET')
    )
    api = API(
        auth, wait_on_rate_limit=True,
        wait_on_rate_limit_notify=True
    )
    try:
        api.verify_credentials()
        print("Authentication OK")
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


class Retweet(StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)

keywords = ["#Sad", "Tweepy"] # filters could be hashtags, regular words, etc


if __name__ == '__main__':
    api = create_app()
    tweets_listener = Retweet(api)
    stream = Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])
