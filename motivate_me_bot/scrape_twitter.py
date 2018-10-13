import tweepy
import json
import wget
import os
import sys
from pprint import pprint
import shutil
import requests
from requests_oauthlib import OAuth1

from keys import *
from text_color import *
from screen_tweets import *
from image_sizing import *
from text_sizing import *
from text_filtering import *

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

def find_image(api, query, output_dir='downloaded/', resolution='large', min_dimensions = (1440, 1080), lang='en', count=100):
    while True:
        results = search_keyword(api, query)
        for tweet in results:
            tweet_dict = vars(tweet)['_json']
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
                    tweet_id_str = tweet_dict['id_str']
                    full_text = tweet_dict['full_text']
                    if check_appropriate(name, screen_name, full_text):
                        url = media_dict['media_url_https'] + ':' + resolution

                        filename = output_dir + url.split('/')[-1][:-(1 + len(resolution))]

                        # Avoid reading potentially large images all at once
                        response = requests.get(url, stream=True)
                        with open(filename, 'wb') as outfile:
                            shutil.copyfileobj(response.raw, outfile)
                        del response

                        # Check whether the image is good (for color / tweet content)
                        img = get_image(filename)
                        print('Image:', full_text)
                        if screen_image_tweet(img, name, screen_name, full_text):
                            return name, screen_name, tweet_id_str, filename
    return -1

def find_quote(api, img, query, lang='en', count=100):
    while True:
        results = search_keyword(api, query)
        for tweet in results:
            tweet_dict = vars(tweet)['_json']
            # Check whether tweet is retweet -- if so, point to retweet instead
            if 'retweeted_status' in tweet_dict.keys():
                tweet_dict = tweet_dict['retweeted_status']
            name = tweet_dict['user']['name']
            screen_name = tweet_dict['user']['screen_name']
            tweet_id_str = tweet_dict['id_str']
            full_text = tweet_dict['full_text']
            if check_appropriate(name, screen_name, full_text):
                filtered_text = filter_quote(full_text)
                if screen_quote_tweet(img, name, screen_name, filtered_text):
                    return name, screen_name, tweet_id_str, filtered_text
    return -1

if __name__ == '__main__':
    api = setup_api()
    query = "#nature"
    print(find_quote(api, query))
    print(find_media(api, query))
