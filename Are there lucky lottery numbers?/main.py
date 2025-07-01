from lottery import OzLotto
import matplotlib.pyplot as plt
from collections import defaultdict
import random as r

if __name__ == "__main__":
    
    max_twice_min_results: int = 0

    iterations: int = 10000
    draws: int = 1636
    # Simulate draws
    for _ in range(iterations):
        if _ % 100 == 0:
            print(f"{_}/{iterations} done")
        results: defaultdict[int,int] = defaultdict(int)
        for _ in range(draws):
            prediction: list[int] = [r.randint(1,47) for _ in range(7)]
            ozlotto = OzLotto()
            correctnums: int = 0
            for val in ozlotto.get_results():
                results[val] += 1
                if val in prediction: # type: ignore
                    correctnums += 1
        if max(results.values()) >= 2*min(results.values()):
            max_twice_min_results += 1


    print((100*max_twice_min_results)/iterations)

    # # Sort the results by number (1 to 47)
    # numbers = list(range(1, 48))
    # frequencies = [100*(results[num]/(draws*9)) for num in numbers] # for %
    # # frequencies = [results[num] for num in numbers] # for count

    # # print(correct_guessed_results)

    # plt.figure(figsize=(12, 6))
    # plt.bar(numbers, frequencies)
    # plt.xticks(numbers)
    # plt.xlabel("Oz Lotto Number")
    # plt.ylabel(f"Frequency in {draws} Draws")
    # plt.title(f"Oz Lotto Number Frequency Distribution ({draws} Simulations)")
    # plt.grid(axis='y', linestyle='--', alpha=0.7)
    # plt.tight_layout()
    # plt.show()
