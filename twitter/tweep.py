#!/usr/bin/env python
"""
pip install tweepy
"""
import sys
import os
import json
import tweepy

# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.


class StreamListener(tweepy.StreamListener):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        with open(self.filename, "w", encoding="utf-8") as f:
            f.write("date,location,user,is_retweet,is_quote,text,quoted_text,tweet_url\n")
    def on_status(self, status):
        print(status.id_str)
        # if "retweeted_status" attribute exists, flag this tweet as a retweet.
        is_retweet = hasattr(status, "retweeted_status")
        if is_retweet:
            return

        # check if text has been truncated
        if hasattr(status, "extended_tweet"):
            text = status.extended_tweet["full_text"]
        else:
            text = status.text

        # check if this is a quote tweet.
        is_quote = hasattr(status, "quoted_status")
        quoted_text = ""
        if is_quote:
            # check if quoted tweet's text has been truncated before recording it
            if hasattr(status.quoted_status, "extended_tweet"):
                quoted_text = status.quoted_status.extended_tweet["full_text"]
            else:
                quoted_text = status.quoted_status.text

        # remove characters that might cause problems with csv encoding
        remove_characters = [",", "\n"]
        for c in remove_characters:
            text.replace(c, " ")
            quoted_text.replace(c, " ")

        tweet_url = f"https://twitter.com/{status.user.screen_name}/status/{status.id}"

        # # debug
        # import pdb
        # pdb.set_trace()
        with open(self.filename, "a", encoding="utf-8") as f:
            f.write("%s,%s,%s,%s,%s,%s,%s, %s\n" % (status.created_at, status.user.location, status.user.screen_name, is_retweet, is_quote, text, quoted_text, tweet_url))

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()

def get_api():
    cred = json.load(open(os.path.expanduser('~/.cred/twitter/cred.json')))
    # authorization tokens
    consumer_key = cred['consumer_key']
    consumer_secret = cred['consumer_secret']
    access_key = cred['access_token_key']
    access_secret = cred['access_token_secret']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    return tweepy.API(auth)

from ratelimit import limits, sleep_and_retry

_period_seconds = 15 * 60 # 15 minutes
@sleep_and_retry
@limits(calls=15, period=_period_seconds)
def api_following(api, username, cursor, count):
    return api.friends(username, cursor=cursor, count=count)

def get_all_following(username):
    # following is called friends: api.friend_ids() then iterate.
    # see api.rate_limit_status() # I think
    api = get_api()
    d = list()
    cursor = -1
    while cursor != 0:
        print(f'calling {cursor} count is {len(d)}')
        page, (prev, cursor) = api_following(api, username, cursor, 100)
        d.extend([x._json for x in page])
    return d


def main(tags="coronavirus,hospital,turning away,died,dead,death,covid,covid-19", filename_prefix=None):
    if filename_prefix is None:
        filename_prefix = tags
    tags = tags.split(',')
    api = get_api()
    # initialize stream
    filename = 'tweep_' + filename_prefix + '.csv'
    streamListener = StreamListener(filename)
    stream = tweepy.Stream(auth=api.auth, listener=streamListener, tweet_mode="extended")
    stream.filter(track=tags)

import argh
if __name__ == "__main__":
    argh.dispatch_command(main)
    # # complete authorization and initialize API endpoint
    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_key, access_secret)
    # api = tweepy.API(auth)

    # # initialize stream
    # streamListener = StreamListener()
    # stream = tweepy.Stream(auth=api.auth, listener=streamListener, tweet_mode="extended")
    # with open("out.csv", "w", encoding="utf-8") as f:
    #     f.write("date,location,user,is_retweet,is_quote,text,quoted_text,tweet_url\n")
    # tags = ["coronavirus", "hospital", "turning away", "died", "dead", "death", "covid", "covid-19"]
    # stream.filter(track=tags)
