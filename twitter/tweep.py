"""
pip install tweepy
"""
import sys
import os
import json
cred = json.load(open(os.path.expanduser('~/.cred/twitter/cred.json')))
import tweepy

# authorization tokens
consumer_key = cred['consumer_key']
consumer_secret = cred['consumer_secret']
access_key = cred['access_token_key']
access_secret = cred['access_token_secret']

# StreamListener class inherits from tweepy.StreamListener and overrides on_status/on_error methods.


class StreamListener(tweepy.StreamListener):
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
        with open("out.csv", "a", encoding="utf-8") as f:
            f.write("%s,%s,%s,%s,%s,%s,%s, %s\n" % (status.created_at, status.user.location, status.user.screen_name, is_retweet, is_quote, text, quoted_text, tweet_url))

    def on_error(self, status_code):
        print("Encountered streaming error (", status_code, ")")
        sys.exit()


def main(tags="coronavirus,hospital,turning away,died,dead,death,covid,covid-19", filename_prefix='out'):
    tags = tags.split(',')
    # tags = ["coronavirus", "hospital", "turning away", "died", "dead", "death", "covid", "covid-19"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener, tweet_mode="extended")
    filename = filename_prefix + '.csv'
    with open(filename, "w", encoding="utf-8") as f:
        f.write("date,location,user,is_retweet,is_quote,text,quoted_text,tweet_url\n")
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
