#!/usr/bin/env python
# encoding: utf-8

import pandas as pd
import argh
import csv
import os
import json
cred = json.load(open(os.path.expanduser('~/.cred/twitter/cred.json')))
import tweepy

# authorization tokens
consumer_key = cred['consumer_key']
consumer_secret = cred['consumer_secret']
access_key = cred['access_token_key']
access_secret = cred['access_token_secret']


def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)

    # save most recent tweets
    alltweets.extend(new_tweets)

    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s" % (oldest))

        # all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        print("...%s tweets downloaded so far" % (len(alltweets)))

    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text] for tweet in alltweets]
    # outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    filename = f'{screen_name}_tweets.csv'
    df = pd.DataFrame(outtweets, columns=['id', 'created_at', 'text'])
    df.to_csv(filename, index=False)
    # # write the csv
    # with open("%s_tweets.csv" % screen_name, "wb") as f:
    #     writer = csv.writer(f)
    #     writer.writerow([b"id", b"created_at", b"text"])
    #     writer.writerows(outtweets)

if __name__ == "__main__":
    # pass in the username of the account you want to download
    # get_all_tweets("J_tsar")
    argh.dispatch_command(get_all_tweets)
