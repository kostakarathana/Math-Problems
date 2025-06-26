from quicksort import QuickSort
from standardsort import StandardSort
from naivesort import NaiveSort
import random as r
import matplotlib.pyplot as plt

if __name__ == "__main__":
    low = 1
    high = 1000
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

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(12, 7), dpi=120) # type: ignore 

    ax.plot(range(low, high, step), qs_times, label="QuickSort", linewidth=2.5, color='#1f77b4', marker='o', markersize=4) # type: ignore 
    ax.plot(range(low, high, step), std_times, label="StandardSort", linewidth=2.5, color='#ff7f0e', marker='s', markersize=4) # type: ignore 
    ax.plot(range(low, high, step), naive_times, label="NaiveSort", linewidth=2.5, color='#2ca02c', marker='^', markersize=4) # type: ignore 

    ax.set_yscale('log') # type: ignore 
    ax.set_xlabel('List Size', fontsize=16, fontweight='bold', color='#333333') # type: ignore 
    ax.set_ylabel('Milliseconds Taken (log scale)', fontsize=16, fontweight='bold', color='#333333') # type: ignore 
    ax.set_title('Sorting Algorithm Performance Comparison', fontsize=20, fontweight='bold', color='#222222', pad=20) # type: ignore 
    ax.legend(fontsize=14, frameon=True, fancybox=True, shadow=True, borderpad=1) # type: ignore 
    ax.grid(True, which='both', linestyle='--', linewidth=0.7, alpha=0.7) # type: ignore 

    # Add background gradient
    ax.set_facecolor("#000000")
    fig.patch.set_facecolor("#afafff")

    # Tweak tick params
    ax.tick_params(axis='both', which='major', labelsize=13, colors='#444444') # type: ignore 
    plt.tight_layout()
    plt.show() # type: ignore 



    