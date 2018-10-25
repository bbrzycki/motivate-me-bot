import sys
import os
sys.path.append(os.path.dirname(__file__))

from blur import draw_box, constant_blur, gradient_blur
from draw import draw_quote_in_box, draw_signature, draw_credits
from image_sizing import get_image, get_boundary, get_box_corners
from scrape_twitter import setup_api, search_keyword, find_image, find_quote
from screen_tweets import is_website, contains_hashtag, contains_emoji, \
    is_punctuation, ends_with_punctuation, is_appropriate, check_quote_quality, \
    screen_image_tweet, screen_quote_tweet
from text_filtering import filter_quote
from text_formatting import fit_text_to_box
from text_sizing import quote_width, signature_width, credit_width, full_credits_width, \
    check_quote_width, check_footer_width
from text_color import average_color, average_contrast_color, get_all_luminances, \
    overall_contrast_color, select_region_and_color, check_image_colors
from run_pipeline import create_combined_image, upload_image
from determine_tweet_content import attribution_text, attribution_length, find_hashtags
