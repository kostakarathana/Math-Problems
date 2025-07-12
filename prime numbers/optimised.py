import matplotlib.pyplot as plt
import math
import time

def get_primes_to_n(n: int) -> list[int]:
    output: list[int] = []
    for i in range(2,n+1):
        i_is_prime = True
        for j in range(2,int(math.sqrt(i))+1):
            if i % j == 0:
                i_is_prime = False
                break
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

    # [9.5367431640625e-07, 0.00017118453979492188, 0.00032067298889160156, 0.0004992485046386719, 0.0008099079132080078, 0.0010058879852294922, 0.0013279914855957031, 0.0014541149139404297, 0.0017828941345214844, 0.0019199848175048828]
    

