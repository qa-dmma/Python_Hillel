# 3. Nested lists

list1 = [1, 2, 3, 4, 5, 6]
list2 = [1, 2, 3]
list3 = [1, 2, 3, 4, 5]
list4 = [1]
list5 = []
list6 = [1, 2, 3, 4, 5, 6, 7]


def listInLists(input_list):
    result = [[], []]
    if len(input_list) <= 1:
        result = [input_list, []]
        return str(input_list) + " => " + str(result)
    else:
        x = 0
        if len(input_list) % 2 == 0:
            while x < len(input_list) / 2:
                result[0].append(input_list[x])
                x += 1
            while x >= len(input_list) / 2 and x != len(input_list):
                result[1].append(input_list[x])
                x += 1
        else:
            while x <= len(input_list) / 2:
                result[0].append(input_list[x])
                x += 1
                while x >= len(input_list) / 2 and x != len(input_list):
                    result[1].append(input_list[x])
                    x += 1
    return str(input_list) + " => " + str(result)


print(listInLists(list1))
print(listInLists(list2))
print(listInLists(list3))
print(listInLists(list4))
print(listInLists(list5))
print(listInLists(list6))
