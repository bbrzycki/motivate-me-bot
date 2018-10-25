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
