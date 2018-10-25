from context import motivatemebot as mmb

def test_website():
    assert mmb.is_website('https://www.google.com') == True
    assert mmb.is_website('Not a website!') == False
    assert mmb.is_website('http://insecure.website.com') == True
    assert mmb.is_website('') == False

def test_hashtag():
    assert mmb.contains_hashtag('#test') == True
    assert mmb.contains_hashtag('test') == False
    assert mmb.contains_hashtag('') == False

def test_punctuation():
    for char in '.,/?!\'"\n#@$% ':
        assert mmb.is_punctuation(char) == True
    assert mmb.is_punctuation('a') == False
    assert mmb.is_punctuation('hi!') == False

def test_ends_with_punctuation():
    # Excluding newline characters
    assert mmb.ends_with_punctuation('hi') == False
    assert mmb.ends_with_punctuation('hi.') == True
    assert mmb.ends_with_punctuation('hi.hi') == False
    assert mmb.ends_with_punctuation('hi\n') == False
    assert mmb.ends_with_punctuation('hi\n\n') == False
    assert mmb.ends_with_punctuation('hi.\n') == True
    assert mmb.ends_with_punctuation('hi!\n\n') == True

def is_appropriate():
    assert mmb.is_appropriate('John Doe', 'johndoe', 'Subscribe to my account!', tweet_type='quote') == False
    assert mmb.is_appropriate('John Doe', 'johndoe', 'To be or not to be, that is the question.', tweet_type='quote') == True
    assert mmb.is_appropriate('John Doe', 'johndoe', 'Go to my YouTube account for lots of inspiration.', tweet_type='quote') == False
    assert mmb.is_appropriate('John Doe', 'johndoe', 'Quote of the day: to be or not to be!', tweet_type='quote') == False
    assert mmb.is_appropriate('John Doe', 'johndoe', 'This is a wonderful way to approach your day.', tweet_type='quote') == False
    assert mmb.is_appropriate('John Doe', 'johndoe', 'To be or not to be #motvation #instagram #quote', tweet_type='quote') == False
