# 1. Calculator

template_string = str("Агов, вводь тільки цифри ок ?")
operation_dict = {
    0: {"name": "Сума", },
    1: {"name": "Віднімання", },
    2: {"name": "Ділення", },
    3: {"name": "Множення", },
}
while True:
    try:
        input_value_one = int(input("Введіть перше число: "))
        input_value_two = int(input("Введіть друге число: "))
        break
    except ValueError:
        print(template_string)
print("Який порядок повинен бути?")
print("1: ", "Перше значення ->", input_value_one, "| математична операція |", input_value_two, "<- Друге значення")
print("2: ", "Друге значення ->", input_value_two, "| математична операція |", input_value_one, "<- Перше значення")
while True:
    try:
        math_question = int(input("1 чи 2 ? "))
        if math_question in (1, 2):
            break
        else:
            print("Будь ласка, введіть тільки 1 або 2")
    except ValueError:
        print(template_string)
print("Доступні математичні дії:\n",
      operation_dict[0]["name"], "\n",
      operation_dict[1]["name"], "\n",
      operation_dict[2]["name"], "\n",
      operation_dict[3]["name"])
math_operation = str(input("Що обираємо ? "))
if math_operation == operation_dict[0]["name"]:
    print("Результат суми: ", input_value_one + input_value_two)
elif math_operation == operation_dict[1]["name"]:
    if math_question == 1:
        print("Результат віднімання ", input_value_one - input_value_two)
    else:
        print("Результат віднімання ", input_value_two - input_value_one)
elif math_operation == operation_dict[2]["name"]:
    if input_value_one == 0 or input_value_two == 0:
        print("Кернес би вами пишався :D\nМатематичні операції з нулем при діленні заборонені!")
    else:
        if math_question == 1:
            print("Результат ділення: ", bool(input_value_one / input_value_two))
        else:
            print("Результат ділення: ", bool(input_value_two / input_value_one))
elif math_operation == operation_dict[3]["name"]:
    if input_value_one == 0 or input_value_two == 0:
        print("Математичні операції з нулем при множенні заборонені!")
    else:
        print("Результат множення: ", input_value_one * input_value_two)
else:
    print("Ой, ви щось не то ввели!")
