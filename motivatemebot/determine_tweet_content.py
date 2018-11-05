import datetime
import os
import random

import regex

def attribution_text(image_screen_name,
                     image_tweet_id_str,
                     quote_screen_name,
                     quote_tweet_id_str):
    return 'Image: @%s (https://twitter.com/%s/status/%s) | ' % (image_screen_name, image_screen_name, image_tweet_id_str) \
        + 'Quote: @%s (https://twitter.com/%s/status/%s)' % (quote_screen_name, quote_screen_name, quote_tweet_id_str)

def attribution_length(image_screen_name, quote_screen_name):
    # Links on Twitter are shortened to 23 characters no matter what,
    # so this is the correct length of the tweet before hashtags are included
    return 8 * 2 + len(image_screen_name) + len(quote_screen_name) + 9 + 2 * 23

def find_hashtags(image_keyword, quote_keyword, quote, char_limit=60):
    remaining_char = char_limit

    remove = regex.compile(r'[\p{C}|\p{M}|\p{P}|\p{S}|\p{Z}]+', regex.UNICODE)
    keywords = '%s %s' % (image_keyword, quote_keyword)
    hashtag_list = remove.sub(' ', keywords).split()
    remaining_char -= 3 + len(image_keyword) + len(quote_keyword)

    day_of_the_week = datetime.datetime.today().weekday()
    daily_hashtags = []
    if day_of_the_week == 0:
        daily_hashtags.append('MondayMotivation')
        daily_hashtags.append('MondayMood')
    elif day_of_the_week == 1:
        daily_hashtags.append('TipTuesday')
        daily_hashtags.append('TuesdayMotivation')
    elif day_of_the_week == 2:
        daily_hashtags.append('WisdomWednesday')
        daily_hashtags.append('WednesdayMotivation')
    elif day_of_the_week == 3:
        daily_hashtags.append('ThursdayThoughts')
        daily_hashtags.append('ThursdayMotivation')
    elif day_of_the_week == 4:
        daily_hashtags.append('FearlessFriday')
        daily_hashtags.append('FridayMotivation')
    elif day_of_the_week == 5:
        daily_hashtags.append('SaturdayMotivation')
        daily_hashtags.append('SaturdayMood')
    else:
        daily_hashtags.append('SundayMood')
        daily_hashtags.append('SundayMotivation')
        daily_hashtags.append('ThinkBIGSundayWithMarsha')

    remaining_char -= sum([2 + len(w) for w in daily_hashtags])
    hashtag_list.extend(daily_hashtags)

    if remaining_char > 2:
        with open(os.path.join(os.path.dirname(__file__), 'hashtag-words.txt'), 'r') as f:
            hashtag_words = f.read().split('\n')
            random.shuffle(hashtag_words)
            min_len = min([len(w) for w in hashtag_words])
            for word in hashtag_words:
                if remaining_char < 2 + min_len:
                    break
                if len(word) >= 4 and 2 + len(word) <= remaining_char:
                    hashtag_list.append(word.lower())
                    remaining_char -= 2 + len(word)
    hashtag_list = list(set(hashtag_list))
    return '#' + ' #'.join(hashtag_list)
