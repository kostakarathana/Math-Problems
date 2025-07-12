import matplotlib.pyplot as plt

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
    plt.plot(get_primes_to_n(1000))
    plt.show()

