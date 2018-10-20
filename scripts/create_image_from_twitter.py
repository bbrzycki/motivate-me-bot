'''
Scrapes Twitter and uploads a motivational image to the @MotivateMeBot account.

Run this script from the scripts/ directory
'''

import sys
import os
import errno
sys.path.append('../')

import numpy as np

import motivate_me_bot as mmb

if __name__ == '__main__':
    download_dir = 'images/'
    new_dir = 'new_images/'

    quote_keyword = '#motivation'
    image_keyword = '#sunset'

    quote_font_file = "../fonts/AppleChancery.ttf"
    footer_font_file = "../fonts/AppleGothic.ttf"

    image_screen_name, image_tweet_id_str, quote_screen_name, \
        quote_tweet_id_str, hashtag_str, new_image_filename = mmb.create_combined_image(image_keyword,
                                                                quote_keyword,
                                                                download_dir,
                                                                new_dir,
                                                                quote_font_file=quote_font_file,
                                                                footer_font_file=footer_font_file,
                                                                show=False)

    print('\nImage saved at %s.' % new_image_filename)
    mmb.upload_image(image_screen_name,
                     image_tweet_id_str,
                     quote_screen_name,
                     quote_tweet_id_str,
                     hashtag_str,
                     new_image_filename,
                     upload=False)
