import html
from emoji import UNICODE_EMOJI

from autocorrect import spell
import ftfy
from unidecode import unidecode


from check_tweets import (contains_emoji, contains_hashtag,
                          ends_with_punctuation, is_punctuation, is_website)


def process_quote(full_text, autocorrect=False, verbose=False):
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

    # First pass nuke for removing trailing hashtags
    while (len(word_list) != 0
           and contains_hashtag(word_list[-1])
           and not ends_with_punctuation(word_list[-1])):
        del word_list[-1]

    # Delete trailing hashtags. Bot requires a certain length of text,
    # so starting checks at the second to last index is ok.
    i = len(word_list) - 1
    j = i - 1
    while j > 0 and contains_hashtag(word_list[j]):
        if ends_with_punctuation(word_list[j]):
            del word_list[j + 1:i + 1]
            i = j
            j = i - 1
        else:
            j -= 1
    if (j >= 0
        and contains_hashtag(word_list[j + 1])
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

    # Removing trailing periods with newlines.. this is more common than
    # I would expect
    while (len(word_list) != 0
           and word_list[-1] == '.\n'):
        del word_list[-1]

    # If a new line does *not* have punctuation, then add it,
    # otherwise don't add anything. Match using regex.
    for i in range(len(word_list)):
        # if word_list[i] != '':
        try:
            if i == 0:
                word_list[i] = word_list[i][0].upper() + word_list[i][1:]
            if word_list[i] != '' and word_list[i][-1] == '\n':
                if len(word_list[i]) >= 2 and not is_punctuation(word_list[i][-2]):
                    if i == len(word_list) - 1:
                        word_list[i] = word_list[i][:-1] + '.'
                    elif word_list[i + 1] != '' and word_list[i + 1][0].islower():
                        word_list[i] = word_list[i][:-1] + ','
                    else:
                        word_list[i] = word_list[i][:-1] + '.'
                else:
                    word_list[i] = word_list[i][:-1]
                    if i < len(word_list) - 1 and not word_list[i][-1] in ',:;-' and len(word_list[i + 1]) >= 2:
                        word_list[i + 1] = word_list[i + 1][0].upper() + word_list[i + 1][1:]
            if (i == len(word_list) - 1
                    and not (ends_with_punctuation(word_list[i])
                             or word_list[i][0].isupper()
                             or word_list[i][0].isdigit())):
                word_list[i] = word_list[i] + '.'
        except Exception:
            pass
    if verbose:
        print(word_list)

    # Guarantee punctuation if there is an attribution to the quote
    for i, word in enumerate(word_list):
        if word in ['-', '~', '--', '~~'] and i >= len(word_list) - 4:
            if not ends_with_punctuation(word_list[i - 1]):
                word_list[i - 1] += '.'

    filtered = ' '.join(word_list)
    if verbose:
        print(filtered)
        print('-'*20)
    return filtered


def process_name(name, verbose=False):
    if verbose:
        print(name)
    name = html.unescape(name).replace('\xa0', ' ').replace('#', ' #')
    name = ftfy.fix_text(name)

    if verbose:
        print(name)

    # Remove emojis
    no_emoji = []
    for char in name:
        if char not in UNICODE_EMOJI:
            no_emoji.append(char)
    name = ''.join(no_emoji)

    # Convert to closest ascii characters
    name = unidecode(name)

    if verbose:
        print(name)

    return name.strip()
