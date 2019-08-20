from context import motivatemebot as mmb


def test_processing():
    inputs = ['this is a test tweet',
              'a multiline test\n on whether it correctly adds punctuation\nThere should be a period before this',
              'Get rid of hashtags! #one #two #three',
              'Get rid of hashtags! #one #two\n #three',
              'Get rid of hashtags #one #two #three…',
              'But not #all of #them! #one #two #three…',
              'But it #should remove #enough #of #them! - Wise Person #one #two #three. #four #five/ #six']
    outputs = ['This is a test tweet.',
               'A multiline test, on whether it correctly adds punctuation. There should be a period before this.',
               'Get rid of hashtags!',
               'Get rid of hashtags!',
               'Get rid of hashtags.',
               'But not all of them!',
               'But it should remove enough of them! - Wise Person']
    for input, output in zip(inputs, outputs):
        assert mmb.process_quote(input) == output
