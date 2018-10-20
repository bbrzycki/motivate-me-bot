import sys
import os
import errno

import numpy as np

from blur import *
from draw import *
from image_sizing import *
from scrape_twitter import *
from text_color import *
from screen_tweets import *
from text_filtering import *
from text_formatting import *
from text_sizing import *
from determine_tweet_content import *

def create_combined_image(image_keyword='#sunset',
                          quote_keyword='#motivation',
                          download_dir='images/',
                          new_dir='new_images/',
                          quote_font_file='Apple Chancery.ttf',
                          footer_font_file='AppleGothic.ttf',
                          show=False):
    if download_dir[-1] != '/':
        download_dir = download_dir + '/'
    try:
        os.makedirs(download_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    if new_dir[-1] != '/':
        new_dir = new_dir + '/'
    try:
        os.makedirs(new_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    api = setup_api()

    print('Finding image...')
    image_name, image_screen_name, image_tweet_id_str, image_filename = find_image(api,
                                                               image_keyword,
                                                               footer_font_file,
                                                               output_dir=download_dir,
                                                               min_dimensions=(1440, 1080))

    img = get_image(image_filename)
    img_width, img_height = img.size
    boundary = get_boundary(img)

    print('Selecting text region and color...')
    location, color = select_region_and_color(img)
    box_corners = get_box_corners(img, location=location)

    print('Finding quote...')
    quote_name, quote_screen_name, quote_tweet_id_str, quote = find_quote(api,
                                                                img,
                                                                quote_keyword,
                                                                quote_font_file=quote_font_file,
                                                                footer_font_file=footer_font_file)

    print('Fitting quote to image...')
    all_lines, font_size, spacing, max_char_height = fit_text_to_box(box_corners,
                                                                     quote,
                                                                     quote_font_file=quote_font_file,
                                                                     equal_spacing=True)

    print('Writing quote to image...')
    # Actually draw onto image
    draw_quote_in_box(img,
                      box_corners,
                      all_lines,
                      quote_font_file,
                      font_size,
                      color=color,
                      spacing=spacing,
                      equal_spacing=True,
                      max_char_height=max_char_height,
                      draw_box=False)

    print('Writing signature to image...')
    draw_signature(img, footer_font_file=footer_font_file)

    print('Writing credits to image...')
    draw_credits(img,
                 quote_name,
                 quote_screen_name,
                 image_name,
                 image_screen_name,
                 footer_font_file=footer_font_file)

    print('Finished creating image!')
    new_image_filename = new_dir + os.path.split(image_filename)[1]
    img.save(new_image_filename)

    if show:
        img.show()

    print('Determining hashtags...')
    char_limit = 279 - attribution_length(image_screen_name, quote_screen_name)
    hashtag_str = find_hashtags(image_keyword,
                                quote_keyword,
                                quote,
                                char_limit=char_limit)

    return image_screen_name, image_tweet_id_str, \
        quote_screen_name, quote_tweet_id_str, hashtag_str, new_image_filename

def upload_image(image_screen_name,
                 image_tweet_id_str,
                 quote_screen_name,
                 quote_tweet_id_str,
                 hashtag_str,
                 new_image_filename,
                 upload=True):
    api = setup_api()
    tweet_text = '%s %s' % (attribution_text(image_screen_name,
                                             image_tweet_id_str,
                                             quote_screen_name,
                                             quote_tweet_id_str),
                            hashtag_str)
    print('\nStatus:\n\n%s\n' % tweet_text)
    if upload:
        api.update_with_media(new_image_filename, status=tweet_text)
        print('~ Uploaded to Twitter! ~')
    else:
        print('~ Not uploaded to Twitter ~')
