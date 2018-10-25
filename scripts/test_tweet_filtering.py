from context import motivatemebot as mmb

if __name__ == '__main__':
    try:
        # Get API keys stored as environmental variables
        from os import environ
        CONSUMER_KEY = environ['CONSUMER_KEY']
        CONSUMER_SECRET = environ['CONSUMER_SECRET']
        ACCESS_TOKEN = environ['ACCESS_TOKEN']
        ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
    except KeyError:
        # Otherwise, get API keys stored in a hidden script keys.py in this directory
        from keys import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET

    api = mmb.setup_api(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    query = '#motivation'
    results = mmb.search_keyword(api, query)

    for tweet in results:

        tweet_dict = vars(tweet)['_json']
        # Check whether tweet is retweet -- if so, point to retweet instead
        if 'retweeted_status' in tweet_dict.keys():
            tweet_dict = tweet_dict['retweeted_status']
        name = tweet_dict['user']['name']
        screen_name = tweet_dict['user']['screen_name']
        full_text = tweet_dict['full_text']

        print('='*20)
        print(name, screen_name, full_text)
        print(mmb.check_appropriate(name, screen_name, full_text))
        filtered_text = mmb.filter_quote(full_text)
        print(filtered_text)
        print('='*20)
        if mmb.check_appropriate(name, screen_name, full_text):
            print("YES")
            break
        else:
            print("NO")
