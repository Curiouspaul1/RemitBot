from tweepy import API, OAuthHandler
import os
from dotenv import load_dotenv
import logging, time
load_dotenv()

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



def find_tweets(api):
    tweets = api.mentions_timeline()
    tweets = [
        tweet for tweet in tweets if tweet.in_reply_to_status_id is None \
             and tweet.retweeted is False
    ]
    for tweet in tweets:
        print(tweet.text)
        try:
            tweet.retweet()
            tweet.favorite()
            print("Done")
        except Exception as e:
            print("Error Trying to retweet or like")

if __name__ == '__main__':
    api = create_app()
    while True:
        find_tweets(api)
        time.sleep(20)
