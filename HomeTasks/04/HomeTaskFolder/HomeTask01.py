# 1. Moving zero value/values at the end of list

list1 = [0, 1, 0, 12, 3]
list2 = [0]
list3 = [1, 0, 13, 0, 0, 0, 5]
list4 = [9, 0, 7, 31, 0, 45, 0, 45, 0, 45, 0, 0, 96, 0]


def moving(dataList):
    dataList.sort(key=lambda x: x == 0)
    return dataList


print(moving(list1))
print(moving(list2))
print(moving(list3))
print(moving(list4))
