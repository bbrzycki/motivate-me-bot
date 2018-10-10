from image_sizing import *
from text_color import *

def screen_quote(full_text):
    return True

def filter_quote(full_text):
    return full_text

def screen_image(filename):
    img = get_image(filename)
    if not check_image_colors(img):
        return False
    return True
