import matplotlib.pyplot as plt
import math
import time

def get_primes_to_n(n: int) -> list[int]:
    sieve = [True] * (n + 1)
    sieve[0:2] = [False, False]  # 0 and 1 are not prime

    for i in range(2, int(math.sqrt(n)) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False

    return [i for i, is_prime in enumerate(sieve) if is_prime]

if __name__ == "__main__":
    times = []
    for i in range(1,10000,1000):
        start = time.time()
        res = get_primes_to_n(i)
        times.append(time.time()-start)
    print(times)
    
    # [4.0531158447265625e-06, 3.1948089599609375e-05, 6.198883056640625e-05, 9.179115295410156e-05, 0.0001270771026611328, 0.0001552104949951172, 0.0001938343048095703, 0.00023508071899414062, 0.0002598762512207031, 0.00031113624572753906]