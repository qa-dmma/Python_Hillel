# 3. Unique value

def find_unique_value(some_list):
    for x in some_list:
        if some_list.count(x) == 1:
            return x
    return None


assert find_unique_value([1, 2, 1, 1]) == 2, 'Test1'
assert find_unique_value([2, 3, 3, 3, 5, 5]) == 2, 'Test2'
assert find_unique_value([5, 5, 5, 2, 2, 0.5]) == 0.5, 'Test3'
assert find_unique_value([5, 5, 5, 2, 2]) is None, 'Test4'
print("ОК")
