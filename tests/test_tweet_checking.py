from context import motivatemebot as mmb


def test_website():
    assert mmb.is_website('https://www.google.com')
    assert not mmb.is_website('Not a website!')
    assert mmb.is_website('http://insecure.website.com')
    assert not mmb.is_website('')


def test_hashtag():
    assert mmb.contains_hashtag('#test')
    assert not mmb.contains_hashtag('test')
    assert not mmb.contains_hashtag('')


def test_punctuation():
    for char in '.,/?!\'"\n#@$% ':
        assert mmb.is_punctuation(char)
    assert not mmb.is_punctuation('a')
    assert not mmb.is_punctuation('hi!')


def test_ends_with_punctuation():
    # Excluding newline characters
    assert not mmb.ends_with_punctuation('hi')
    assert mmb.ends_with_punctuation('hi.')
    assert not mmb.ends_with_punctuation('hi.hi')
    assert not mmb.ends_with_punctuation('hi\n')
    assert not mmb.ends_with_punctuation('hi\n\n')
    assert mmb.ends_with_punctuation('hi.\n')
    assert mmb.ends_with_punctuation('hi!\n\n')


def is_appropriate():
    assert not mmb.is_appropriate('John Doe', 'johndoe', 'Subscribe to my account!', tweet_type='quote')
    assert mmb.is_appropriate('John Doe', 'johndoe', 'To be or not to be, that is the question.', tweet_type='quote')
    assert not mmb.is_appropriate('John Doe', 'johndoe', 'Go to my YouTube account for lots of inspiration.', tweet_type='quote')
    assert not mmb.is_appropriate('John Doe', 'johndoe', 'Quote of the day: to be or not to be!', tweet_type='quote')
    assert not mmb.is_appropriate('John Doe', 'johndoe', 'This is a wonderful way to approach your day.', tweet_type='quote')
    assert not mmb.is_appropriate('John Doe', 'johndoe', 'To be or not to be #motvation #instagram #quote', tweet_type='quote')
