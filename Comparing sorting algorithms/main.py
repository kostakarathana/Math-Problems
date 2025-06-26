from quicksort import QuickSort
from standardsort import StandardSort
import random as r
import matplotlib.pyplot as plt

if __name__ == "__main__":
    low = 1
    high = 5000
    step = 1
    qs_times: list[float] = []
    std_times: list[float] = []

    for i in range(low, high, step):
        randlist1 = [r.randint(1,10000) for _ in range(i)]
        randlist2 = [r.randint(1,10000) for _ in range(i)]
        randlist3 = [r.randint(1,10000) for _ in range(i)]

        quicksort1: QuickSort = QuickSort(randlist1)
        quicksort1.sort(True)
        stdsort1: StandardSort = StandardSort(randlist1)
        stdsort1.sort(True)
 
        quicksort2: QuickSort = QuickSort(randlist2)
        quicksort2.sort(True)
        stdsort2: StandardSort = StandardSort(randlist2)
        stdsort2.sort(True)

        quicksort3: QuickSort = QuickSort(randlist3)
        quicksort3.sort(True)
        stdsort3: StandardSort = StandardSort(randlist3)
        stdsort3.sort(True)


        qs_average = (quicksort1.return_time_taken() + quicksort2.return_time_taken() + quicksort3.return_time_taken())
        std_average = (stdsort1.return_time_taken() + stdsort2.return_time_taken() + stdsort3.return_time_taken())
        qs_times.append(qs_average)
        std_times.append(std_average)
        print(f"{i}/{high}")
    

    plt.plot(qs_times, label="QuickSort")
    plt.plot(std_times, label="StandardSort")
    plt.legend()
    plt.show()


    