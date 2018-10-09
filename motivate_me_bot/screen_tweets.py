from image_sizing import *
from text_color import *

def screen_quote(full_text):
    return True

def filter_quote(full_text):
    return full_text

def screen_image(filename, min_dimensions = (1000, 600)):
    img = get_image(filename)
    img_width, img_height = img.size
    min_width, min_height = min_dimensions
    if img_width < min_width or img_height < min_height:
        return False
    if not check_image_colors(img):
        return False
    return True
