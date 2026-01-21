# 4. “Calculating a discount”

item_price = int(input("Введіть ціну товару: "))
item_discount = float(input("Введіть розмір знижки: "))

print("Ціна зі знижкою: ", item_price - (item_price * (item_discount / 100)))
