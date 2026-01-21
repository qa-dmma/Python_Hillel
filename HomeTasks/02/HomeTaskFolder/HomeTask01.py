# 1. Square of a number.

print("Використовуємо ціле число?")
decision = input("Так/Ні: \n")
if decision == "Так":
    number = int(input("Введіть ціле число: "))
    print("Квадрат введеного числа: ", number ** 2)
elif decision == "Ні":
    number = float(input("Введіть число з крапкою: "))
    print("Квадрат введеного числа: ", round(number ** 2, 2))
else:
    print("Умови вводу не виконані")
