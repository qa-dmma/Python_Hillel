# 1. Calculator

firstInput = float(input("Введіть перше число: "))
operation = input("Введіть дію (+, -, *, /): ")
secondInput = float(input("Введіть друге число: "))

if operation == "+":
    result = firstInput + secondInput
    print("Результат:", result)

elif operation == "-":
    result = firstInput - secondInput
    print("Результат:", result)

elif operation == "*":
    result = firstInput * secondInput
    print("Результат:", result)

elif operation == "/":
    if secondInput == 0:
        print("Помилка: ділення на нуль!")
    else:
        result = firstInput / secondInput
        print("Результат:", result)

else:
    print("Невідома операція!")
