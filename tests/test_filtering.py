from context import motivatemebot as mmb

def test_filtering():
    inputs = ['this is a test tweet',
              'a multiline test\n on whether it correctly adds punctuation\n There should be a period before this',
              'Get rid of hashtags! #one #two #three',
              'Get rid of hashtags! #one #two\n #three',
              'Remove website https://www.google.com from tweet',
              'Get rid of hashtags #one #two #three…',
              'But not #all of #them! #one #two #three…']
    outputs = ['This is a test tweet.',
               'A multiline test, on whether it correctly adds punctuation. There should be a period before this.',
               'Get rid of hashtags!',
               'Get rid of hashtags!',
               'Remove website from tweet.',
               'Get rid of hashtags.',
               'But not all of them!']
    for input, output in zip(inputs, outputs):
        assert mmb.filter_quote(input) == output
