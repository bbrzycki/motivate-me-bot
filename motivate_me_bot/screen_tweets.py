from image_sizing import *
from text_sizing import *
from text_formatting import *
from text_color import *

def check_appropriate(name, screen_name, full_text):
    return True

def screen_image_tweet(img, name, screen_name, full_text):
    return check_image_colors(img) \
        and check_footer_width(img, name, screen_name) \
        and check_appropriate(name, screen_name, full_text)

def screen_quote_tweet(img, name, screen_name, full_text):
    return check_text_widths(img, name, screen_name, full_text) \
        and check_appropriate(name, screen_name, full_text)

def filter_quote(full_text):
    return full_text
