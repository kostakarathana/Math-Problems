from functools import lru_cache
import time
import matplotlib.pyplot as plt


def fib_wo_cache(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib_wo_cache(n-1) + fib_wo_cache(n-2)

@lru_cache
def fib_w_cache(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fib_w_cache(n-1) + fib_w_cache(n-2)

def timetest(f, n):
    start_time = time.time()
    for i in range(100):
        f(n)
    return time.time() - start_time

values_and_speed = {}

for i in range(1, 10):
    values_and_speed.update({i: (timetest(fib_wo_cache, i)) / (timetest(fib_w_cache, i))})

plt.plot(values_and_speed.values())
plt.title("speed of caching vs no caching in fibonacci sequence")
plt.xticks(range(len(values_and_speed)), labels=values_and_speed.keys())
plt.show()
