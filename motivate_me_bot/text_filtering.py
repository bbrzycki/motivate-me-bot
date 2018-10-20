from screen_tweets import *

import sys
import os
import regex
from autocorrect import spell

def filter_quote(full_text, autocorrect=False):
    '''Filter the tweet to be more presentable as a standalone quote'''
    # If a new line does *not* have punctuation, then add it,
    # otherwise don't add anything. Match using regex.
    lines = full_text.split('\n')
    lines[:] = [line for line in lines if line != '']

    punctuation = regex.compile(r'[\p{C}|\p{M}|\p{P}|\p{S}|\p{Z}]+', regex.UNICODE)
    for i in range(len(lines)):
        if i == 0:
            lines[i] = lines[i][0].upper() + lines[i][1:]
        if punctuation.match(lines[i].strip()[-1]) is None:
            if i == len(lines) - 1:
                lines[i] = lines[i].strip() + '.'
            elif lines[i + 1].strip()[0].islower():
                lines[i] = lines[i].strip() + ','
            else:
                lines[i] = lines[i].strip() + '.'
        else:
            if i < len(lines) - 1:
                lines[i + 1] = lines[i + 1][0].upper() + lines[i + 1][1:]
    word_list = ' '.join(lines).split()
    print('-'*20)
    print(full_text)
    print(word_list)
    new_list = []
    for word in word_list:
        if not check_website(word) and not check_emoji(word):
            new_list.append(word)
    word_list = new_list
    print(word_list)
    while check_hashtag(word_list[-1]):
        del word_list[-1]
    print(word_list)
    for i, word in enumerate(word_list):
        if check_hashtag(word):
            word_list[i] = word[1:]
        if autocorrect:
            try:
                word_list[i] = spell(word_list[i])
            except AttributeError:
                pass

    print(word_list)
    filtered = ' '.join(word_list)
    print(filtered)

    print('-'*20)
    return filtered
