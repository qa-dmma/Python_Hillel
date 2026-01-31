# 1. String formatting
import keyword

user_input = str(input("Ведіть строку: "))


def rules(string):
    if not string:
        return False

    if string in keyword.kwlist:
        return False

    if string[0].isdigit():
        return False

    if any(letter.isupper() for letter in string):
        return False

    if string != "_" and not string.replace("_", "").isalnum():
        return False

    if "__" in string:
        return False

    return True


print(rules(user_input))
