import tweepy
import json
import wget
import os
import sys
import errno
from pprint import pprint
import requests
from requests_oauthlib import OAuth1

from keys import *
from text_color import *
from screen_tweets import *

def setup_api():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def search_keyword(api, query, lang='en', count=100):
    '''
    Search Twitter for tweets containing the query keyword.
    '''
    results = api.search(q=query, lang=lang, count=count, tweet_mode='extended')
    return results

def find_quote(api, query, lang='en', count=100):
    results = search_keyword(api, query)
    for tweet in results:
        tweet_dict = vars(tweet)['_json']
        full_text = tweet_dict['full_text']
        if screen_quote(full_text):
            # Check whether tweet is a retweet
            if full_text[0:2] != 'RT':
                name = tweet_dict['user']['name']
                screen_name = tweet_dict['user']['screen_name']
            elif 'retweeted_status' in tweet_dict.keys():
                retweet_dict = tweet_dict['retweeted_status']
                name = retweet_dict['user']['name']
                screen_name = retweet_dict['user']['screen_name']
                full_text = retweet_dict['full_text']
            else:
                continue
            return name, screen_name, filter_quote(full_text)
    return -1

def find_image(api, query, output_dir='downloaded/', lang='en', count=100):
    try:
        os.makedirs(output_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    results = search_keyword(api, query)
    for tweet in results:
        tweet_dict = vars(tweet)['_json']
        full_text = tweet_dict['full_text']
        if screen_quote(full_text):
            # Check whether tweet is retweet -- if so, point to retweet instead
            if full_text[0:2] == 'RT':
                tweet_dict = tweet_dict['retweeted_status']
            # Check if the tweet contains media
            if 'extended_entities' in tweet_dict.keys():
                if tweet_dict['extended_entities']['media'][0]['type'] == 'photo':
                    print(tweet_dict['extended_entities']['media'][0])
                    name = tweet_dict['user']['name']
                    screen_name = tweet_dict['user']['screen_name']
                    url = tweet_dict['extended_entities']['media'][0]['media_url_https']
                    filename = wget.download(url, out=output_dir)
                    # TODO: Filter out "bad" images
                    if screen_image(filename):
                        return name, screen_name, filename
    return -1

if __name__ == '__main__':
    api = setup_api()
    query = "#nature"
    print(find_quote(api, query))
    print(find_media(api, query))
