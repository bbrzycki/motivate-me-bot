from screen_tweets import is_website, contains_hashtag, contains_emoji, \
    is_punctuation, ends_with_punctuation, is_appropriate, check_quote_quality, \
    screen_image_tweet, screen_quote_tweet

import sys
import os
import regex
import html
from autocorrect import spell

def filter_quote(full_text, autocorrect=False):
    '''Filter the tweet to be more presentable as a standalone quote'''

    # Unescaping html characters (such as &amp and &quot), and manually replace
    # &nbsp ('\xa0'). Further, make sure hashtags get split even if they
    # accidentally don't have whitespace in the original tweet.
    escaped = html.unescape(full_text).replace('\xa0', ' ').replace('#', ' #')

    # Split by words, but keep newline character with the word at the end of
    # each line (to handle line-ending punctuation later).
    stripped = '\n '.join([line.strip() for line in escaped.split('\n')])
    word_list = [word for word in stripped.split(' ') if word != '\n' and word != '']
    print('-'*20)
    print(full_text)
    print(word_list)
    new_list = []
    for word in word_list:
        if not is_website(word) and not contains_emoji(word):
            new_list.append(word)
    word_list = new_list
    print(word_list)
    while contains_hashtag(word_list[-1]) and not ends_with_punctuation(word_list[-1]):
        del word_list[-1]
    print(word_list)
    for i, word in enumerate(word_list):
        if contains_hashtag(word):
            word_list[i] = word[1:]
        if autocorrect:
            try:
                word_list[i] = spell(word_list[i])
            except AttributeError:
                pass

    # If a new line does *not* have punctuation, then add it,
    # otherwise don't add anything. Match using regex.
    for i in range(len(word_list)):
        if i == 0:
            word_list[i] = word_list[i][0].upper() + word_list[i][1:]
        if word_list[i][-1] == '\n':
            if not is_punctuation(word_list[i][-2]):
                if i == len(word_list) - 1:
                    word_list[i] = word_list[i][:-1] + '.'
                elif word_list[i + 1][0].islower():
                    word_list[i] = word_list[i][:-1] + ','
                else:
                    word_list[i] = word_list[i][:-1] + '.'
            else:
                if i < len(word_list) - 1:
                    word_list[i] = word_list[i][:-1]
                    word_list[i + 1] = word_list[i + 1][0].upper() + word_list[i + 1][1:]
        elif i == len(word_list) - 1 and not is_punctuation(word_list[i][-1]):
            word_list[i] = word_list[i] + '.'

    print(word_list)
    filtered = ' '.join(word_list)
    print(filtered)

    print('-'*20)
    return filtered
