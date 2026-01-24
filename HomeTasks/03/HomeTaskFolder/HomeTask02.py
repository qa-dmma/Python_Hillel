# 2. Swapping numbers

list1 = [12, 3, 4, 10]
list2 = [1]
list3 = []
list4 = [12, 3, 4, 10, 8]


def moveValueList(input_list):
    if len(input_list) <= 1:
        return str(input_list) + " => " + str(input_list)
    else:
        temp_list = input_list.copy()
        last = input_list.pop()
        input_list.insert(0, last)
        return str(temp_list) + " => " + str(input_list)


print(moveValueList(list1))
print(moveValueList(list2))
print(moveValueList(list3))
print(moveValueList(list4))
