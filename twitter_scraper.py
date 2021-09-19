import tweepy
import csv
from utils import *


# settings
num_threads = 250

####input your credentials here
consumer_key = 'kQWhgi3L2dKrxqS5rFB04LS2Q'
consumer_secret = 'JF4YP8j1fAwlBUnILdz4dRFWfnX4edzqGRTs05EoyjR8e1Kdjf'
access_token = '1329878486526402560-8nz9qHI46mTHOJ4iQ6Paa3QTzBYrnn'
access_token_secret = 'Tkm4qhy6op9KwdDu71RxCTuet7nTs3VmNsKCIwFONYfxF'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


# establish company list
company_list = []

conversations = []

company_reply_counter = 0

for company in company_list:
    twitter_id = company['twitter_id']
    threads_collected = 0

    for tweet in tweepy.Cursor(api.search, q="from:{} -filter:retweets".format(twitter_id),
                               lang="nl",
                               since="2020-01-01", tweet_mode='extended').items(1000):  # count=1000

        # define target, likes, shares
        in_reply_to = 'none'
        favourite_count = '0'
        retweet_count = '0'
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            in_reply_to = tweet.in_reply_to_status_id_str
            company_reply_counter += 1

        if hasattr(tweet, 'favorite_count'):
            favourite_count = tweet.favorite_count
        if hasattr(tweet, 'retweet_count'):
            retweet_count = tweet.retweet_count

        print(tweet.created_at, tweet.user.name, tweet.full_text, favourite_count, retweet_count, in_reply_to)

        # Open/Create a file to append data
        with open(''+'.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([tweet.created_at, tweet.user.name, tweet.full_text.encode('utf-8'), favourite_count, in_reply_to])