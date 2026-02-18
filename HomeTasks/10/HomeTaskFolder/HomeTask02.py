def first_word(text: str) -> str:
    """
    Find first word from string


    :param text: String sentence
    :return: String first word
    """

    def strip_left(input_string: str) -> str:
        """
        Truncates symbols at the start of a line


        :param input_string: String sentence with symbols
        :return: String sentence without symbols
        """
        while input_string and not input_string[0].isalpha():
            input_string = input_string[1:]
        return input_string

    def take_word(input_string: str) -> str:
        """
        Find first word from string


        :param input_string: String sentence
        :return: String first word
        """
        temp_string = ""
        for x in input_string:
            if x.isalpha() or x == "'":
                temp_string += x
            else:
                break
        return temp_string

    trimmed_text = strip_left(text)
    return take_word(trimmed_text)


assert first_word("Hello world") == "Hello", 'Test1'
assert first_word("greetings, friends") == "greetings", 'Test2'
assert first_word("don't touch it") == "don't", 'Test3'
assert first_word(".., and so on ...") == "and", 'Test4'
assert first_word("hi") == "hi", 'Test5'
assert first_word("Hello.World") == "Hello", 'Test6'
print('OK')

