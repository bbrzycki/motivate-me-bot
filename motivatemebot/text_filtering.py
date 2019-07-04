import html
import os
import sys

import regex
from autocorrect import spell
import ftfy

from screen_tweets import (check_quote_quality, contains_emoji,
                           contains_hashtag, ends_with_punctuation,
                           is_appropriate, is_punctuation, is_website,
                           screen_image_tweet, screen_quote_tweet)


def filter_quote(full_text, autocorrect=False, verbose=False):
    '''Filter the tweet to be more presentable as a standalone quote'''

    # Unescaping html characters (such as &amp and &quot), and manually replace
    # &nbsp ('\xa0'). Further, make sure hashtags get split even if they
    # accidentally don't have whitespace in the original tweet.
    escaped = html.unescape(full_text).replace('\xa0', ' ').replace('#', ' #')
    escaped = escaped.replace('…', '')

    # Unicode fixing with ftfy package
    escaped = ftfy.fix_text(escaped)

    # Split by words, but keep newline character with the word at the end of
    # each line (to handle line-ending punctuation later).
    stripped = '\n '.join([line.strip() for line in escaped.split('\n')])
    word_list = [word for word in stripped.split(' ') if word != '\n' and word != '']
    if verbose:
        print('-'*20)
        print(full_text)
        print(word_list)
    new_list = []
    for word in word_list:
        if not is_website(word) and not contains_emoji(word):
            # if not contains_emoji(word):
            split_words = []
            start_index = 0
            for i in range(0, len(word)):
                if word[i] in ['.', ',', '!', '?'] and i != len(word) - 1:
                    if not is_punctuation(word[i + 1]) and not word[i + 1] == ' ':
                        split_words.append(word[start_index:(i + 1)])
                        start_index = i + 1
            if start_index != len(word):
                split_words.append(word[start_index:])
            for split_word in split_words:
                new_list.append(split_word)
    word_list = new_list
    if verbose:
        print(word_list)

    #
    # # Track number of ending hashtags; observed that there are quite a few
    # # tweets that have punctuative erroneously at the end
    # words_betw_end_punc = []
    # hash_betw_end_punc = []
    # num_words = 0
    # num_hashtags = 0
    # punc_indices = [-1]
    # for i, word in enumerate(word_list):
    #     if word[-1] in ['.', '!', '?']:
    #         punc_indices.append(i)
    #         words_betw_end_punc.append(num_words)
    #         hash_betw_end_punc.append(num_hashtags)
    #         num_words = 0
    #         num_hashtags = 0
    #     else:
    #         num_words += 1
    #         if contains_hashtag(word):
    #             num_hashtags += 1
    # words_betw_end_punc.append(num_words)
    # hash_betw_end_punc.append(num_hashtags)
    # punc_indices.append(len(word_list) - 1)
    # # Go from reverse to take elements off of the end. The second a phrase
    # # separated by ending punctuation *isn't* completely filled with
    # # hashtags, then exit; perhaps the actual tweet is doing that by design.
    # if verbose:
    #     print(word_list)
    # for i in range(1, len(punc_indices))[::-1]:
    #     if hash_betw_end_punc[i - 1] == words_betw_end_punc[i - 1]:
    #         del word_list[punc_indices[i - 1] + 1:punc_indices[i] + 1]
    #     else:
    #         break
    # hashtag_tail = True
    # for i in range(max(-5, -len(word_list)), 0):
    #     if not contains_hashtag(word_list[i]):
    #         hashtag_tail = False
    # if hashtag_tail:
    #     while (contains_hashtag(word_list[-1])
    #            and not ends_with_punctuation(word_list[-1])
    #            and not word_list[-1][0].isupper()
    #            and not word_list[-1][0].isdigit()):
    #         del word_list[-1]

    # First pass nuke for removing trailing hashtags
    while contains_hashtag(word_list[-1]) and not ends_with_punctuation(word_list[-1]):
        del word_list[-1]

    i = len(word_list) - 1
    j = i - 1
    while j > 0 and contains_hashtag(word_list[j]):
        if ends_with_punctuation(word_list[j]):
            del word_list[j + 1:i + 1]
            i = j
            j = i - 1
        else:
            j -= 1
    if (contains_hashtag(word_list[j + 1])
        and (ends_with_punctuation(word_list[j])
             or word_list[j][0].isupper()
             or word_list[j][0].isdigit())):
        del word_list[j + 1:i + 1]

    if verbose:
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
                word_list[i] = word_list[i][:-1]
                if i < len(word_list) - 1 and not word_list[i][-1] in ',:;-':
                    word_list[i + 1] = word_list[i + 1][0].upper() + word_list[i + 1][1:]
        if (i == len(word_list) - 1
                and not (ends_with_punctuation(word_list[i])
                         or word_list[i][0].isupper()
                         or word_list[i][0].isdigit())):
            word_list[i] = word_list[i] + '.'
    if verbose:
        print(word_list)
    filtered = ' '.join(word_list)
    if verbose:
        print(filtered)
        print('-'*20)
    return filtered
