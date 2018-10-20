from image_sizing import *
from text_sizing import *
from text_formatting import *
from text_color import *

import sys
import os

import string
import regex

def check_website(text):
    return 'http' in text and '://' in text

def check_hashtag(text):
    return text[0] == '#'

def check_appropriate(name, screen_name, full_text):
    '''
    Check whether the tweet uses inappropriate language (or keywords that are
    otherwise good to exclude, such as promotional material)
    '''
    exclude_words = []
    with open(os.path.join(os.path.dirname(__file__), 'bad-words.txt'), 'r') as f:
        bad_words = f.read()
        exclude_words.extend(bad_words.split('\n'))
    with open(os.path.join(os.path.dirname(__file__), 'spam-twitter-words.txt'), 'r') as f:
        spam_words = f.read()
        exclude_words.extend(spam_words.split('\n'))

    all_text = "%s %s %s" % (name, screen_name, full_text)

    remove = regex.compile(r'[\p{C}|\p{M}|\p{P}|\p{S}|\p{Z}]+', regex.UNICODE)
    all_text = remove.sub(' ', all_text)

    word_list = all_text.replace('\n', ' ').split()
    for word in exclude_words:
        if word.lower() in [w.lower() for w in word_list]:
            return False

    return True

def check_quote_quality(full_text):
    '''Somehow determine the "quality" of the resulting quote'''
    if len(full_text.split()) < 8:
        return False
    return True

def screen_image_tweet(img, name, screen_name, footer_font_file='AppleGothic.ttf'):
    '''Check whether the image is good enough to use'''
    return check_image_colors(img) \
        and check_footer_width(img, name, screen_name, footer_font_file=footer_font_file)

def screen_quote_tweet(img,
                       name,
                       screen_name,
                       full_text,
                       quote_font_file='Apple Chancery.ttf',
                       footer_font_file='AppleGothic.ttf'):
    '''Check whether the quote is good enough to use'''
    return check_quote_quality(full_text) \
        and check_footer_width(img, name, screen_name, footer_font_file=footer_font_file) \
        and check_quote_width(img, name, screen_name, full_text, quote_font_file=quote_font_file)
