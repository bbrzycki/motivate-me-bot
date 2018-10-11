import sys
sys.path.append('../')
from pprint import pprint
import motivate_me_bot as mmb

if __name__ == '__main__':
    api = mmb.setup_api()

    query = '#motivation'
    tweet = mmb.search_keyword(api, query)[0]

    tweet_dict = vars(tweet)['_json']
    # Check whether tweet is retweet -- if so, point to retweet instead
    if 'retweeted_status' in tweet_dict.keys():
        tweet_dict = tweet_dict['retweeted_status']
    full_text = tweet_dict['full_text']

    print(full_text)
    print(mmb.filter_quote(full_text))
