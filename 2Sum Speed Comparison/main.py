import time
import matplotlib.pyplot as plt


def unoptimal(n: list, target: int) -> bool:
    for i in range(len(n)):
        for j in range(len(n)):
            if n[i] + n[j] == target and i != j:
                return True
    return False

def optimal(n: list, target: int) -> bool:
    comps = set()
    for i in range(len(n)):
        if n[i] in comps:
            return True
        comps.add(target-n[i])
    return False

if __name__ == "__main__":
    tests = [
        ([1, 2, 3, 2, 1], 3, True),
        ([1, 6, 3, 2, 1], 100, False),
        ([1, 3], 4, True),
        ([1, 1], 1, False)
    ]

    for test in tests:
        if unoptimal(test[0], test[1]) != test[2]:
            print("Fail!")
        elif optimal(test[0], test[1]) != test[2]:
            print("Fail! (optimal)")

    unoptimal_runtimes = []
    optimal_runtimes = []

    unoptimal_ops = [0]
    optimal_ops = [0]

    start_i = 0
    end_i = 100

    for i in range(start_i, end_i):
        if i % 100 == 0:
            print(f"{i}/{end_i} done")
        start = time.time()
        for j in range(i):
            if True:
                optimal_ops.append(optimal_ops[-1] + 1)
        optimal_runtimes.append(time.time() - start)

        start = time.time()
        for j in range(i):
            for x in range(i):
                if True:
                    unoptimal_ops.append(unoptimal_ops[-1] + 1)
        unoptimal_runtimes.append(time.time() - start)

    relative = []
    print(end_i-start_i)
    for i in range(end_i-start_i):
        if optimal_runtimes[i] == 0:
            relative.append(0)
            continue
        relative.append(unoptimal_runtimes[i]/optimal_runtimes[i])

    # plt.plot(relative)

    plt.plot(unoptimal_ops)
    plt.plot(optimal_ops)

    #
    plt.show()















