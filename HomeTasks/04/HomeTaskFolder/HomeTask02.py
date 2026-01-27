# 2. Sum of elements with even indices multiplied by the last one

list1 = [0, 1, 7, 2, 4, 8]
list2 = [1, 3, 5]
list3 = [6]
list4 = []


def calculation(list):
    if len(list) != 0:
        return sum(list[::2] * list[-1])
    else:
        return 0


print(calculation(list1))
print(calculation(list2))
print(calculation(list3))
print(calculation(list4))
