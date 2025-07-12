import matplotlib.pyplot as plt
import math
import time

def get_primes_to_n(n: int) -> list[int]:
    output: list[int] = []
    for i in range(2,n+1):
        i_is_prime = True
        for j in range(2,i):
            if i % j == 0:
                i_is_prime = False
        if i_is_prime:
            output.append(i)
    return output


if __name__ == "__main__":
    times = []
    for i in range(1,10000,1000):
        start = time.time()
        res = get_primes_to_n(i)
        times.append(time.time()-start)
    print(times)

    # [0.0, 0.008818864822387695, 0.03531789779663086, 0.08530831336975098, 0.1536867618560791, 0.2437119483947754, 0.35575127601623535, 0.48294782638549805, 0.6317870616912842, 0.8031010627746582]


