from image_sizing import *
from text_sizing import *
from text_formatting import *
from text_color import *

import sys
import os

import string
import regex
from emoji import UNICODE_EMOJI

def is_website(text):
    return 'http' in text and '://' in text

def contains_hashtag(text):
    return text[0] == '#'

def contains_emoji(text):
    for emoji in UNICODE_EMOJI:
        if emoji in text:
            return True
    return False

def is_punctuation(char):
    punctuation = regex.compile(r'[\p{C}|\p{M}|\p{P}|\p{S}|\p{Z}]+', regex.UNICODE)
    if punctuation.match(char) is None:
        return False
    return True

def ends_with_punctuation(text):
    i = -1
    while text[i] == '\n':
        i -= 1
    return is_punctuation(text[i])

def is_appropriate(name, screen_name, full_text, tweet_type='quote'):
    '''
    Check whether the tweet uses inappropriate language (or keywords that are
    otherwise good to exclude, such as promotional material)
    '''
    # Exclude a few characters that generally correspond to lower quality quotes
    if tweet_type == 'quote':
        bad_char = '@?$'
        for char in bad_char:
            if char in full_text:
                return False

    # Built list of words to exclude from text
    exclude_words = []
    with open(os.path.join(os.path.dirname(__file__), 'bad-words.txt'), 'r') as f:
        bad_words = f.read()
        exclude_words.extend(bad_words.split('\n'))
    if tweet_type == 'quote':
        with open(os.path.join(os.path.dirname(__file__), 'spam-twitter-words.txt'), 'r') as f:
            spam_words = f.read()
            exclude_words.extend(spam_words.split('\n'))

    # Name can have multiple words, so compare this alongside tweet text
    all_text = "%s %s %s" % (name, screen_name, full_text)

    # Replace punctuation with spaces using regex
    remove = regex.compile(r'[\p{C}|\p{M}|\p{P}|\p{S}|\p{Z}]+', regex.UNICODE)
    all_text = remove.sub(' ', all_text).lower()
    all_text = ' '.join(all_text.strip())

    # Compare all excluded words / phrases to all relevant text
    for word in exclude_words:
        stripped = word.strip().lower()
        # Check word (separated by spaces), force lowercase to prevent case issues
        compare_string = ' ' + stripped + ' '
        if stripped != '' and compare_string in all_text:
            return False

    # TODO: Decide how to exclude certain screen names
    # for word in bad_words.split('\n'):
    #     # If bad word appears in any form in the screen_name, return False
    #     if len(word) >= 3 and word in screen_name.lower():
    #         print('screen name', screen_name, word)
    #         return False
    return True

def check_quote_quality(full_text):
    '''Somehow determine the quality of the resulting quote'''
    # Make sure the length of the quote is something substantial
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
