# 4. Search for common elements

def common_elements():
    set1 = set()
    set2 = set()
    for i in range(100):
        if i % 3 == 0:
            set1.add(i)
        if i % 5 == 0:
            set2.add(i)

    return set1.intersection(set2)


assert common_elements() == {0, 75, 45, 15, 90, 60, 30}
