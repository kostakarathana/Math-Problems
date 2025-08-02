import random as r
import matplotlib.pyplot as plt

def roll_dice() -> int:
    return r.randint(1,6)



if __name__ == "__main__":
    iterations = 1000
    results = {}
    for i in range(1,7):
        results[i] = 0


    for i in range(iterations):
        results[roll_dice()] += 1
    
    plt.bar(results.keys(), results.values())
    plt.xlabel('Dice Face')
    plt.ylabel('Frequency')
    plt.title('Dice Roll Frequencies')
    plt.show()
    



