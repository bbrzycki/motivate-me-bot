def filter_quote(full_text):
    word_list = full_text.replace('\n', ' ').split(' ')
    print(word_list)
    for i, word in enumerate(word_list):
        if 'http' in word and '://' in word:
            del word_list[i]
    print(word_list)
    while word_list[-1][0] == '#':
        del word_list[-1]
    print(word_list)
    return ' '.join(word_list)
