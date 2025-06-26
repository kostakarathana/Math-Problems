from quicksort import QuickSort
from standardsort import StandardSort
from naivesort import NaiveSort
import random as r
import matplotlib.pyplot as plt

if __name__ == "__main__":
    low = 1
    high = 500
    step = 1

    NUM_TRIALS = 100
    qs_times: list[float] = []
    std_times: list[float] = []
    naive_times: list[float] = []

    for i in range(low, high, step):
        qs_total: float = 0.0
        std_total: float = 0.0
        naive_total: float = 0.0

        for _ in range(NUM_TRIALS):
            randlist = [r.randint(1, 10000) for _ in range(i)]

            quicksort = QuickSort(randlist.copy())
            quicksort.sort(True)
            qs_total += quicksort.return_time_taken()*1000 # milliseconds

            stdsort = StandardSort(randlist.copy())
            stdsort.sort(True)
            std_total += stdsort.return_time_taken()*1000 

            naivesort = NaiveSort(randlist.copy())
            naivesort.sort(True)
            naive_total += naivesort.return_time_taken()*1000 

        qs_times.append(qs_total / NUM_TRIALS)
        std_times.append(std_total / NUM_TRIALS)
        naive_times.append(naive_total / NUM_TRIALS)

        print(f"{i}/{high}")

    plt.plot(range(low, high, step), qs_times, label="QuickSort") #type: ignore
    plt.plot(range(low, high, step), std_times, label="StandardSort")#type: ignore
    plt.plot(range(low, high, step), naive_times, label="NaiveSort")#type: ignore
    plt.yscale('log') #type: ignore
    plt.xlabel('List Size') #type: ignore
    plt.ylabel('Milliseconds Taken (log scale)') #type: ignore
    plt.legend() #type: ignore
    plt.show() #type: ignore



    