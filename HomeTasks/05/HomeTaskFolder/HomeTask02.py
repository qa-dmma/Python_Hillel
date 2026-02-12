# 3. Hashtag from string

import operator

operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}

while True:
    try:
        first = float(input("Введіть перше число: "))
    except ValueError:
        print("Помилка: введіть число")
        continue
    operation = input("Введіть дію (+, -, *, /): ").strip()
    if operation not in operators:
        print("Невідома операція")
        continue
    try:
        second = float(input("Введіть друге число: "))
        if operation == "/" and second == 0:
            print("Ділення на нуль!")
            continue
    except ValueError:
        print("Помилка: введіть число")
        continue

    result = operators[operation](first, second)
    print("Результат:", result)
    if input("Продовжити? (y/yes): ").strip().lower() not in ("y", "yes"):
        break

print("Програма завершена")
