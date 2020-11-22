from tweepy import StreamListener, API, OAuthHandler, Stream
import os
from dotenv import load_dotenv
from twitter_data import TwitterClient
import logging
load_dotenv()


xyz = TwitterClient('@chopra__mudit',with_sentiment=True)
xyz.set_query(input('Enter the word you want to search::  '))
tweets = xyz.get_tweets()
result = []
for i in tweets:
    if i['sentiment'] in set(['Negative', 'negative']):
        result.append(i)
result = result[0:4]
print(result)
            

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

keywords = ["#TheraBotHelp", "Tweepy"] # filters could be hashtags, regular words, etc


def comment(api):
    for i in result:
        print(i)
        api.update_status(
            status="Hey! Hope you are doing good! Please know that we are here for you. You should visit a therapist if you feel like. Here is the link from which you can find a good one - https://www.goodtherapy.org/find-therapist.html",
            in_reply_to_status_id=i['tweet_id']
        )

if __name__ == '__main__':
    api = create_app()
    comment(api)
    tweets_listener = Retweet(api)
    stream = Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])
