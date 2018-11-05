import json
import os
import shutil
import sys
import time
from pprint import pprint

import requests
import tweepy

from image_sizing import get_boundary, get_box_corners, get_image
from screen_tweets import (check_quote_quality, contains_emoji,
                           contains_hashtag, ends_with_punctuation,
                           is_appropriate, is_punctuation, is_website,
                           screen_image_tweet, screen_quote_tweet)
from text_color import (average_color, average_contrast_color,
                        check_image_colors, get_all_luminances,
                        overall_contrast_color, select_region_and_color)
from text_filtering import filter_quote
from text_sizing import (check_footer_width, check_quote_width, credit_width,
                         full_credits_width, quote_width, signature_width)

def setup_api(consumer_key, consumer_secret, access_token, access_token_secret):
    '''
    Set up api for Twitter interactions using tweepy.
    '''
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)

def search_keyword(api,
                   query,
                   lang='en',
                   count=100):
    '''
    Search Twitter for tweets containing the query keyword.
    '''
    results = api.search(q=query, lang=lang, count=count, tweet_mode='extended')
    return results

def find_image(api,
               query,
               footer_font_file='AppleGothic.ttf',
               output_dir='downloaded/',
               resolution='large',
               min_dimensions = (1440, 1080),
               lang='en',
               min_follower_count=500,
               count=100,
               verbose=True):
    while True:
        results = search_keyword(api, query, lang=lang, count=count)
        for tweet in results:
            tweet_dict = vars(tweet)['_json']
            # Check whether tweet is retweet -- if so, point to retweet instead
            if 'retweeted_status' in tweet_dict.keys():
                tweet_dict = tweet_dict['retweeted_status']
            # pprint(tweet_dict)
            # Check if the tweet contains media
            if 'extended_entities' in tweet_dict.keys() and tweet_dict['user']['followers_count'] >= min_follower_count:
                media_dict = tweet_dict['extended_entities']['media'][0]
                dimensions = media_dict['sizes'][resolution]
                w, h = dimensions['w'], dimensions['h']
                min_w, min_h = min_dimensions
                if media_dict['type'] == 'photo' and w >= min_w and h >= min_h:
                    name = tweet_dict['user']['name']
                    screen_name = tweet_dict['user']['screen_name']
                    tweet_id_str = tweet_dict['id_str']
                    full_text = tweet_dict['full_text']
                    if is_appropriate(name, screen_name, full_text, tweet_type='image'):
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
                        if screen_image_tweet(img,
                                              name,
                                              screen_name,
                                              footer_font_file=footer_font_file):
                            return name, screen_name, tweet_id_str, filename
        # Wait a bit before searching again
        print('Resuming image search in 60 seconds...')
        time.sleep(60)
    return -1

def find_quote(api,
               img,
               query,
               quote_font_file='Apple Chancery.ttf',
               footer_font_file='AppleGothic.ttf',
               lang='en',
               min_follower_count=500,
               count=100,
               verbose=True):
    while True:
        results = search_keyword(api, query, lang=lang, count=count)
        for tweet in results:
            tweet_dict = vars(tweet)['_json']
            # Check whether tweet is retweet -- if so, point to retweet instead
            if 'retweeted_status' in tweet_dict.keys():
                tweet_dict = tweet_dict['retweeted_status']
            if tweet_dict['user']['followers_count'] >= min_follower_count:
                name = tweet_dict['user']['name']
                screen_name = tweet_dict['user']['screen_name']
                tweet_id_str = tweet_dict['id_str']
                full_text = tweet_dict['full_text']
                if is_appropriate(name, screen_name, full_text, tweet_type='quote'):
                    filtered_text = filter_quote(full_text, verbose=verbose)
                    if screen_quote_tweet(img,
                                          name,
                                          screen_name,
                                          filtered_text,
                                          quote_font_file=quote_font_file,
                                          footer_font_file=footer_font_file):
                        return name, screen_name, tweet_id_str, filtered_text
        # Wait a bit before searching again
        print('Resuming quote search in 60 seconds...')
        time.sleep(60)
    return -1
