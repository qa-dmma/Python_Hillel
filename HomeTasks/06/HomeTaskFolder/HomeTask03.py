# 3. Numbers multiplying

user_input = int(input("Введіть ціле число: "))

while user_input >= 10:
    temp = 1
    for digit in str(user_input):
        temp *= int(digit)
    user_input = temp

print(user_input)
