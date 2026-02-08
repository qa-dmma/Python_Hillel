# 3.Search for a subcontractor

def second_index(text, some_str):
    first_pos = text.find(some_str)
    if first_pos == -1:
        return None

    second_pos = text.find(some_str, first_pos + len(some_str))
    return second_pos if second_pos != -1 else None


assert second_index("sims", "s") == 3, 'Test1'
assert second_index("find the river", "e") == 12, 'Test2'
assert second_index("hi", "h") is None, 'Test3'
assert second_index("Hello, hello", "lo") == 10, 'Test4'
print('ОК')
