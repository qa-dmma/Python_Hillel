# 2. Formatting user input into dd/hh/mm/ss

names = {1: "день", 2: "днів", 3: "дні"}

user_input = int(input("Введіть число котре більше або дорівнює 0 і менше ніж 8640000: "))


def f_input(value):
    hh_formula = 24 * 60 * 60
    mm_formula = 60 * 60
    ss = str((value % hh_formula % mm_formula) % 60).zfill(2)
    mm = str((value % hh_formula % mm_formula) // 60).zfill(2)
    hh = str(value % hh_formula // mm_formula).zfill(2)
    dd = value // hh_formula
    return dd, hh, mm, ss


def day_word(days):
    if 11 <= days % 100 <= 14:
        return names.get(2)
    last = days % 10
    if last == 1:
        return names.get(1)
    if 2 <= last <= 4:
        return names.get(3)
    return names.get(2)


if user_input in range(0, 8640000):
    print(f"{f_input(user_input)[0]} {day_word(f_input(user_input)[0])}, "
          f"{f_input(user_input)[1]}:{f_input(user_input)[2]}:{f_input(user_input)[3]}")
else:
    print("Введене число не в діапазоні!")
