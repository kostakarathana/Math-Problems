'''
Fair six-sided die is rolled until each face is observed at least once. On the average, how many rolls of the die
are needed?
'''

import matplotlib.pyplot as plt
import random as r

dice_sides = [1,2,3,4,5,6]
seen = [False, False, False, False, False, False]

def get_count_till_all_seen():
    count = 0
    seen = [False, False, False, False, False, False]
    while False in seen:
        count += 1
        num = r.choice(dice_sides)
        seen[num-1] = True
    return count

counts = []

for _ in range(1000000):
    counts.append(get_count_till_all_seen())

print(sum(counts)/1000000)
# plt.hist(counts)
# plt.show()



