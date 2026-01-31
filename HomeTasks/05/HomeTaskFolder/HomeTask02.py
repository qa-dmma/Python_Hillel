#3. Hashtag from string

import operator

operators = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv
}

cycle = "y"

while cycle == "y":
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
    while True:
        cycle = input("Продовжити? (y/n): ").strip().lower()
        if cycle in ["y", "n"]:
            break
        else:
            print("Помилка: введіть 'y' або 'n'")

print("Програма завершена")
