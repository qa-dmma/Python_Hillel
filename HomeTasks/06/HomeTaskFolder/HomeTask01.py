# 1. Return chars between inputted user symbols
import string

user_string = input("Введіть дві літери через дефіс: ").strip()

char_index = (string.ascii_letters.find(user_string[0]), string.ascii_letters.find(user_string[-1]))
start_position = char_index[0]
string_output = ""

if char_index[0] == char_index[-1]:
    string_output = string.ascii_letters[char_index[0]]
else:
    while start_position <= char_index[-1]:
        string_output += string.ascii_letters[start_position]
        start_position += 1

print(string_output)
