import tweepy
import json
import wget
import os
import sys
import errno
from pprint import pprint
import shutil
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
            # Check whether tweet is retweet -- if so, point to retweet instead
            if 'retweeted_status' in tweet_dict.keys():
                tweet_dict = tweet_dict['retweeted_status']
            name = tweet_dict['user']['name']
            screen_name = tweet_dict['user']['screen_name']
            full_text = tweet_dict['full_text']
            return name, screen_name, filter_quote(full_text)
    return -1

def find_image(api, query, output_dir='downloaded/', resolution='large', min_dimensions = (1200, 800), lang='en', count=100):
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
            if 'retweeted_status' in tweet_dict.keys():
                tweet_dict = tweet_dict['retweeted_status']
            # Check if the tweet contains media
            if 'extended_entities' in tweet_dict.keys():
                media_dict = tweet_dict['extended_entities']['media'][0]
                dimensions = media_dict['sizes'][resolution]
                w, h = dimensions['w'], dimensions['h']
                min_w, min_h = min_dimensions
                if media_dict['type'] == 'photo' and w >= min_w and h >= min_h:
                    name = tweet_dict['user']['name']
                    screen_name = tweet_dict['user']['screen_name']
                    url = media_dict['media_url_https'] + ':' + resolution

                    filename = output_dir + url.split('/')[-1][:-(1 + len(resolution))]

                    # Avoid reading potentially large images all at once
                    response = requests.get(url, stream=True)
                    with open(filename, 'wb') as outfile:
                        shutil.copyfileobj(response.raw, outfile)
                    del response

                    # Filter out "bad" images
                    if screen_image(filename):
                        return name, screen_name, filename
    return -1

if __name__ == '__main__':
    api = setup_api()
    query = "#nature"
    print(find_quote(api, query))
    print(find_media(api, query))
