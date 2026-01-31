#2. Supper calculator

import string

user_input = input("Введіть рядок: ")


def check(line):
    line = line.title()
    forbidden_symbols = string.punctuation + " "
    line = "".join(char for char in line if char not in forbidden_symbols)
    if not line.startswith("#"):
        line = "#" + line
    if len(line) > 140:
        return f"Довжина більше 140 символів! Обрізана строка: {line[:140]}"
    return f"Рядок прийнятий: {line}"


print(check(user_input))
