# 3. Random values in lists
import random

list1 = [random.randrange(100) for i in range(random.randint(3, 10))]
list2 = [list1[0], list1[2], list1[-2]].copy()
print(list1, "==", list2)
