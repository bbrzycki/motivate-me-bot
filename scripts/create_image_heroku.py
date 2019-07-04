'''
Scrapes Twitter and uploads a motivational image to the @MotivateMeBot account.

This script is run on Heroku from the home /app/ directory.
'''
from context import motivatemebot as mmb
import sys

def main():
    try:
        # Get API keys stored as environmental variables
        from os import environ
        CONSUMER_KEY = environ['CONSUMER_KEY']
        CONSUMER_SECRET = environ['CONSUMER_SECRET']
        ACCESS_TOKEN = environ['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
    except KeyError:
        # Otherwise, get API keys stored in a hidden script keys.py in this directory
        import sys
        sys.path.append('../')
        from keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

    twitter_api = mmb.setup_api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    download_dir = 'images/'
    new_dir = 'new_images/'

    quote_keyword = '#motivation #inspiration'
    image_keyword = 'nature'

    quote_font_file = "/app/fonts/AppleChancery.ttf"
    footer_font_file = "/app/fonts/AppleGothic.ttf"

    quote_font_file = "../fonts/AppleChancery.ttf"
    footer_font_file = "../fonts/AppleGothic.ttf"

    image_screen_name, image_referral_url, \
        quote_screen_name, quote_referral_url, attribution, \
        hashtag_str, new_image_filename = mmb.create_combined_image(twitter_api,
                                                                    'unsplash',
                                                                    image_keyword,
                                                                    quote_keyword,
                                                                    download_dir,
                                                                    new_dir,
                                                                    quote_font_file=quote_font_file,
                                                                    footer_font_file=footer_font_file,
                                                                    follow_credits=False,
                                                                    show=False)

    print('\nImage saved at %s.' % new_image_filename)
    mmb.upload_image(twitter_api,
                     image_screen_name,
                     image_referral_url,
                     quote_screen_name,
                     quote_referral_url,
                     attribution,
                     hashtag_str,
                     new_image_filename,
                     upload=False)

    return new_image_filename




if __name__ == '__main__':
    main()
