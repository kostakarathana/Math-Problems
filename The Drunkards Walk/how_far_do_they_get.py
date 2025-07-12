import matplotlib.pyplot as plt
import random as r
import math

def get_random_shift():
    angle = r.uniform(0, 2 * math.pi)
    return [math.cos(angle), math.sin(angle)]


final_distances_from_origin: list[float] = []

# Generate walk
for i in range(1000):
    num_steps = 10000
    x, y = [0], [0]
    for _ in range(num_steps):
        dx, dy = get_random_shift()
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)

    final_distances_from_origin.append(math.sqrt(x[-1]**2 + y[-1]**2))


plt.hist(final_distances_from_origin)
plt.show()

