def popular_words(text: str, words: list) -> dict:
    """
    Determine the popularity of certain words in the text


    :param text: string text
    :param words: list of words
    :return: dictionary in format word:quantity
    """
    word_dict = {word: 0 for word in words}
    for item in text.lower().split():
        if item in word_dict:
            word_dict[item] += 1

    return word_dict


assert popular_words('''When I was One I had just begun When I was Two I was nearly new ''',
                     ['i', 'was', 'three', 'near']) == {'i': 4, 'was': 3, 'three': 0, 'near': 0}, 'Test1'
print('OK')
