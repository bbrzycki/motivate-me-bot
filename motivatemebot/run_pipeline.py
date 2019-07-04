import errno
import os

from blur import constant_blur, draw_box, gradient_blur
from determine_tweet_content import (attribution_length, attribution_text,
                                     find_hashtags)
from draw import draw_credits, draw_quote_in_box, draw_signature
from image_sizing import get_boundary, get_box_corners, get_image
from scrape_content import find_twitter_image, find_unsplash_image, find_quote, search_keyword, setup_api
from screen_tweets import (check_quote_quality, contains_emoji,
                           contains_hashtag, ends_with_punctuation,
                           is_appropriate, is_punctuation, is_website,
                           screen_image_tweet, screen_quote_tweet)
from text_color import (average_color, average_contrast_color,
                        check_image_colors, get_all_luminances,
                        overall_contrast_color, select_region_and_color)
from text_filtering import filter_quote
from text_formatting import fit_text_to_box
from text_sizing import (check_footer_width, check_quote_width, credit_width,
                         full_credits_width, quote_width, signature_width)


def create_combined_image(twitter_api,
                          image_method='unsplash',
                          image_keyword='#sunset',
                          quote_keyword='#motivation',
                          download_dir='images/',
                          new_dir='new_images/',
                          quote_font_file='Apple Chancery.ttf',
                          footer_font_file='AppleGothic.ttf',
                          follow_credits=True,
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

    # Getting keys
    try:
        # Get API keys stored as environmental variables
        from os import environ
        UNSPLASH_ACCESS_KEY = environ['UNSPLASH_ACCESS_KEY']
    except KeyError:
        # Otherwise, get API keys stored in a hidden script keys.py in this directory
        import sys
        sys.path.append('../')
        from keys import UNSPLASH_ACCESS_KEY

    print('Finding image...')
    if image_method == 'twitter':
        image_name, image_screen_name, image_referral_url, image_filename = find_twitter_image(twitter_api,
                                                                                               image_keyword,
                                                                                               footer_font_file,
                                                                                               output_dir=download_dir,
                                                                                               min_dimensions=(1440, 1080))
    elif image_method == 'unsplash':
        image_name, image_screen_name, image_referral_url, image_filename = find_unsplash_image(UNSPLASH_ACCESS_KEY,
                                                                                                               image_keyword,
                                                                                                               footer_font_file,
                                                                                                               output_dir=download_dir,
                                                                                                               min_dimensions=(1440, 1080))

    else:
        raise ValueError

    img = get_image(image_filename)

    print('Selecting text region and color...')
    location, color = select_region_and_color(img)
    box_corners = get_box_corners(img, location=location)

    print('Finding quote...')
    quote_name, quote_screen_name, quote_tweet_id_str, quote = find_quote(twitter_api,
                                                                          img,
                                                                          quote_keyword,
                                                                          quote_font_file=quote_font_file,
                                                                          footer_font_file=footer_font_file)
    quote_referral_url = 'https://twitter.com/%s/status/%s' % (quote_screen_name, quote_tweet_id_str)

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
                      box_visible=False)

    print('Writing signature to image...')
    draw_signature(img, footer_font_file=footer_font_file)

    print('Writing credits to image...')
    draw_credits(img,
                 quote_name,
                 quote_screen_name,
                 image_name,
                 image_screen_name,
                 footer_font_file=footer_font_file)

    if follow_credits:
        print('Following image and quote tweeters...')
        if image_method == 'twitter':
            twitter_api.create_friendship(screen_name=image_screen_name)
        twitter_api.create_friendship(screen_name=quote_screen_name)
    else:
        print('Not following image and quote tweeters...')

    print('Finished creating image!')
    new_image_filename = new_dir + os.path.split(image_filename)[1]
    img.save(new_image_filename)

    if show:
        img.show()

    print('Getting attribution section of tweet')
    attribution = attribution_text(image_screen_name,
                                   image_referral_url,
                                   quote_screen_name,
                                   quote_referral_url)

    print('Determining hashtags...')
    char_limit = (279 - len(attribution) + len(image_referral_url)
                  + len(quote_screen_name) - 2 * 23)
    hashtag_str = find_hashtags(image_keyword,
                                quote_keyword,
                                quote,
                                char_limit=char_limit)

    return image_screen_name, image_referral_url, \
        quote_screen_name, quote_referral_url, attribution, hashtag_str, \
        new_image_filename


def upload_image(twitter_api,
                 image_screen_name,
                 image_referral_url,
                 quote_screen_name,
                 quote_referral_url,
                 attribution,
                 hashtag_str,
                 new_image_filename,
                 upload=True):
    tweet_text = '%s %s' % (attribution, hashtag_str)
    print('\nStatus:\n\n%s\n' % tweet_text)
    if upload:
        twitter_api.update_with_media(new_image_filename, status=tweet_text)
        print('~ Uploaded to Twitter! ~')
    else:
        print('~ Not uploaded to Twitter ~')
