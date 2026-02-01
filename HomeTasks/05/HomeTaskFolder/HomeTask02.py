# 3. Hashtag from string

import operator

operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}

cycle = "y"

while cycle == "y" or "yes":
    while True:
        try:
            firstInput = float(input("Введіть перше число: "))
            break
        except:
            print("Помилка: введіть число, а не текст")

    while True:
        operation = input("Введіть дію (+, -, *, /): ").strip()
        if operation in operators:
            break
        else:
            print("Невідома операція")

    while True:
        try:
            secondInput = float(input("Введіть друге число: "))
            if operation == "/" and secondInput == 0:
                print("Ділення на нуль!")
                continue
            break
        except:
            print("Помилка: введіть число, а не текст")

    result = operators[operation](firstInput, secondInput)
    print("Результат:", result)

    cycle = input("Продовжити? (y/yes): ").strip().lower()
    if cycle not in ["y", "yes"]:
        break

print("Програма завершена")
