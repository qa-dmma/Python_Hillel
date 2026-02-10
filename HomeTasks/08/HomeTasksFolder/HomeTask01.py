# 1. Add 1 to the number

def add_one(digits):
    result = digits[:]
    increase = 1
    for item in range(len(result) - 1, -1, -1):
        total = result[item] + increase
        result[item] = total % 10
        increase = total // 10
        if increase == 0:
            break
    if increase:
        result.insert(0, increase)
    return result


assert add_one([1, 2, 3, 4]) == [1, 2, 3, 5], 'Test1'
assert add_one([9, 9, 9]) == [1, 0, 0, 0], 'Test2'
assert add_one([0]) == [1], 'Test3'
assert add_one([9]) == [1, 0], 'Test4'
print("ОК")
