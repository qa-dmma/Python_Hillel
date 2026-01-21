# 7. Printing a number in a column

number_input = input("Введіть чотирьох значне ціле число: ")
char_quantity = len(number_input) - 1
if number_input.find("-") != -1:
    print("Знайдено від'ємне значення:", "-" + str(number_input[int(number_input.find("-")) + 1]),
          "\nДозволений інтервал кожного числа має бути від 0 до 9")
elif len((number_input)) != 4:
    print("Це не чотирьох значне ціле число!")
else:
    errors = 0
    while char_quantity >= 0:
        if not number_input[char_quantity].isdigit():
            errors += 1
        char_quantity -= 1
    if errors == 0:
        output_int = int(number_input)
        print(output_int // 1000)
        print((output_int // 100) % 10)
        print((output_int // 10) % 10)
        print(output_int % 10)
    else:
        print("У рядку присутній символ. Програмний вивід не можливий")
