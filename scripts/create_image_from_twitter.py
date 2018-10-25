'''
Scrapes Twitter and uploads a motivational image to the @MotivateMeBot account.

Run this script from the scripts/ directory
'''
from context import motivatemebot as mmb

if __name__ == '__main__':
    try:
        # Get API keys stored as environmental variables
        from os import environ
        CONSUMER_KEY = environ['CONSUMER_KEY']
        CONSUMER_SECRET = environ['CONSUMER_SECRET']
        ACCESS_TOKEN = environ['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
    except KeyError:
        # Otherwise, get API keys stored in a hidden script keys.py in this directory
        from keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

    api = mmb.setup_api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    download_dir = 'images/'
    new_dir = 'new_images/'

    quote_keyword = '#motivation #inspiration'
    image_keyword = '#sunset'

    quote_font_file = "../fonts/AppleChancery.ttf"
    footer_font_file = "../fonts/AppleGothic.ttf"

    image_screen_name, image_tweet_id_str, quote_screen_name, \
        quote_tweet_id_str, hashtag_str, new_image_filename = mmb.create_combined_image(api,
                                                                image_keyword,
                                                                quote_keyword,
                                                                download_dir,
                                                                new_dir,
                                                                quote_font_file=quote_font_file,
                                                                footer_font_file=footer_font_file,
                                                                follow_credits=False,
                                                                show=False)

    print('\nImage saved at %s.' % new_image_filename)
    mmb.upload_image(api,
                     image_screen_name,
                     image_tweet_id_str,
                     quote_screen_name,
                     quote_tweet_id_str,
                     hashtag_str,
                     new_image_filename,
                     upload=False)
