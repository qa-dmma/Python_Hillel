# 2. “Average of three numbers”

number_one = float(input("Введіть перше число: "))
number_two = float(input("Введіть друге число: "))
number_three = float(input("Введіть третє число: "))

print("Середнє: ", (number_one + number_two + number_three) / 3)

# Або просунутий варіант з вводом як в задачі та форматуванням строки:

# numbers_string = input("Введіть три числа:\n")
#
# numbers_string = numbers_string.replace(",", "")
# numbers_string = numbers_string.replace(" ", "")
#
# char_quantity = len(numbers_string)
# sum_of_numbers = 0
#
# while char_quantity != 0:
#     if numbers_string[char_quantity - 1] != ",":
#         sum_of_numbers += float(numbers_string[char_quantity - 1])
#     char_quantity = char_quantity - 1
#
# print("Середнє: ", sum_of_numbers / len(numbers_string))
