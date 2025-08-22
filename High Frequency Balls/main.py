'''
The lottery often posts statistics on their websites citing
"hot" and "cold" balls that have been drawn from the previous
lotteries. For the Saturday Gold Lotto Australia, their website
says that since 1985, the most popular drawn ball (ball #1) has been drawn 419 times,
whilst ball #44 has been drawn only 330 times. Here's there full distrubution of
drawn numbers as of 22 Aug 2025, with ball #1 at index 0, ball #2 at index 1, etc.

frequencies = [
    419, 358, 370, 362, 386, 386, 394, 407, 366, 363,
    414, 369, 369, 345, 392, 374, 357, 384, 373, 358,
    367, 388, 391, 367, 369, 379, 345, 349, 369, 350,
    366, 372, 378, 376, 360, 373, 363, 373, 355, 390,
    386, 394, 352, 330, 364
]

Even people playing the lottery often talk about
how certain numbers must be 'due' or how some are just plain unlucky.
Through simulation, we can easily tell if there are true lucky numbers.

As of today, there have been 2094 saturdays since 1985. Thus, we can easily see how
likely the distrubution they state is.

Note: I've done a project similar to this before but this is a cleaner redo

RESULTS IN README
'''

import matplotlib.pyplot as plt
import random

BALLS = [i for i in range(1, 46)]

GOLD_LOTTO_FREQUENCIES = [
    419, 358, 370, 362, 386, 386, 394, 407, 366, 363,
    414, 369, 369, 345, 392, 374, 357, 384, 373, 358,
    367, 388, 391, 367, 369, 379, 345, 349, 369, 350,
    366, 372, 378, 376, 360, 373, 363, 373, 355, 390,
    386, 394, 352, 330, 364
]

def simulate_gold_lotto() -> list:
    '''
    Draw 8 numbers from BALLS 2094 times
    '''
    frequencies = [0] * 45
    for i in range(2094):
        for i in range(8):
            frequencies[random.randint(1,44)] += 1
    return frequencies


def plot_and_show_frequencies(frequencies):
    x = list(range(1, len(frequencies) + 1))
    plt.figure(figsize=(14, 6))
    plt.bar(x, frequencies, color="skyblue", edgecolor="black")
    plt.xticks(x)  # show every lotto number
    plt.xlabel("Lotto Number")
    plt.ylabel("Frequency")
    plt.title("Gold Lotto Number Frequencies (Drawn Count)")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_and_show_frequencies(simulate_gold_lotto())
