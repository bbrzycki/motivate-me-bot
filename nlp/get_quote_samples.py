"""
Collect tweets should would pass the non-ML filters and save to a csv for manual labeling.
"""

from context import motivatemebot as mmb
import pandas as pd
import tweepy
import os


def main():
    try:
        # Get API keys stored as environmental variables
        from os import environ
        CONSUMER_KEY = environ['CONSUMER_KEY']
        CONSUMER_SECRET = environ['CONSUMER_SECRET']
        ACCESS_TOKEN = environ['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
    except KeyError:
        # Otherwise, get API keys stored in a hidden script keys.py in this directory
        import sys
        sys.path.append('../')
        from keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

    api = mmb.setup_api(CONSUMER_KEY,
                        CONSUMER_SECRET,
                        ACCESS_TOKEN,
                        ACCESS_TOKEN_SECRET,
                        wait_on_rate_limit=True)

    # quote_keyword = '#motivation #inspiration'
    quote_keyword = '#inspiration'

    # results = mmb.search_keyword(twitter_api,
    #                              quote_keyword,
    #                              lang='en',
    #                              count=100)

    original_text = []
    filtered_text = []
    follower_num = []
    over_500_followers = []
    is_appropriate = []
    tweet_id = []

    num_tweets = 200000

    index = 0
    # try:
    for tweet in tweepy.Cursor(api.search,
                               q=quote_keyword,
                               count=100,
                               tweet_mode='extended').items(num_tweets):
        # for tweet in page:
        tweet_dict = vars(tweet)['_json']
        # Check whether tweet is retweet -- if so, point to retweet instead
        if 'retweeted_status' in tweet_dict.keys():
            tweet_dict = tweet_dict['retweeted_status']

        follower_count = tweet_dict['user']['followers_count']
        follower_num.append(follower_count)
        over_500_followers.append(follower_count >= 500)

        name = tweet_dict['user']['name']
        screen_name = tweet_dict['user']['screen_name']
        tweet_id.append(tweet_dict['id_str'])

        full_text = tweet_dict['full_text']
        original_text.append(full_text)

        is_appropriate.append(mmb.is_appropriate(name, screen_name, full_text,
                                                 tweet_type='quote'))
        filtered_text.append(mmb.filter_quote(full_text, verbose=False))

        print('Finished', index)
        index += 1
    # except Exception:
    #     pass

    print(len(filtered_text),
          len(original_text),
          len(is_appropriate),
          len(over_500_followers),
          len(tweet_id))

    # Automatically grab latest version num
    saved_filenames = os.listdir('quote_data/')
    if len(saved_filenames) == 0:
        version_num = 0
    else:
        last_saved = sorted(saved_filenames)[-1]
        version_num = int(last_saved[-5]) + 1

    labels = [None] * len(original_text)
    almost_labels = [None] * len(original_text)
    df = pd.DataFrame({
        'almost_labels': almost_labels,
        'labels': labels,
        'filtered_text': filtered_text,
        'original_text': original_text,
        'follower_num': follower_num,
        'is_appropriate': is_appropriate,
        'over_500_followers': over_500_followers,
        'tweet_id': tweet_id,
    })
    df = df.loc[list(df.drop('tweet_id', axis=1)
                       .drop('original_text', axis=1)
                       .drop_duplicates()
                       .index)]
    df.to_csv('quote_data/quote_samples%d.csv' % version_num, index=False)
    print('is_appropriate:', sum(is_appropriate))
    print('over_500_followers:', sum(over_500_followers))

    long_enough = df['filtered_text'].fillna('').apply(len) >= 5
    vetted_df = df.loc[df['is_appropriate']
                       & df['over_500_followers']
                       & long_enough]

    filtered_text_set = set()
    for i in range(version_num):
        saved_df = pd.read_csv('quote_data/vetted_quote_samples%d.csv' % i)
        filtered_text_set |= set(saved_df['filtered_text'])

    vetted_df = vetted_df.loc[vetted_df.apply(lambda x: not x['filtered_text'] in filtered_text_set, axis=1)]

    vetted_df.to_csv('quote_data/vetted_quote_samples%d.csv' % version_num)
    print('vetted:', len(vetted_df))


if __name__ == '__main__':
    main()
