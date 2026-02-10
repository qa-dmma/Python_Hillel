# 2. Palindrome
import string


def is_palindrome(text):
    result = text.replace(" ", "").casefold()
    for x in result:
        if x in string.punctuation:
            result = result.replace(x, "")
    return result == result[::-1]


assert is_palindrome('A man, a plan, a canal: Panama') == True, 'Test1'
assert is_palindrome('0P') == False, 'Test2'
assert is_palindrome('a.') == True, 'Test3'
assert is_palindrome('aurora') == False, 'Test4'
print("ОК")
