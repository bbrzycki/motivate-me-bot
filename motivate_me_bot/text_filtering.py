from screen_tweets import *

import sys
import os
from autocorrect import spell

def filter_quote(full_text, autocorrect=False):
    # TODO: If a new line does *not* have punctuation, then add it..
    # Otherwise don't add anything
    word_list = full_text.replace('\n', ' ').split(' ')
    print('-'*20)
    print(full_text)
    print(word_list)
    new_list = []
    for word in word_list:
        if check_website(word):
            pass
        elif word == '':
            pass
        else:
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
