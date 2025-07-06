'''
You are interviewing n candidates for a secretary position.
You can observe each candidate one at a time in random order.
After interviewing each one, you must immediately decide whether to hire them or continue.

You can never go back to a previous candidate, but you can look at past candidates rankings.
For example, you could say, "I haven't seen someone ranked this high yet, this guy must be good!"

Your goal is to maximize the probability of choosing the best candidate (the one with the highest rank).
The higher a candidates rank, the 'better' they are. 

Example: candidates = [24,62,55,93,34,45,13,75,83]

Best candidate is the fourth one in the above list, who's score is 93 (the highest).
'''

import random

class Simulation:
    def __init__(self, n: int) -> None:
        self.n = n
        self.candidates: list[int] = list(range(1, (10*n) + 1))  # Rank 1 (worst) to n (best)
        random.shuffle(self.candidates)  # Random interview order
        self.candidates = self.candidates[::10]
        self.maximum = max(self.candidates)


    def run(self, stop_index: int) -> bool:
        best_seen = max(self.candidates[:stop_index])  # Observe first r candidates
        
        # Select the next candidate better than best_seen
        for c in self.candidates[stop_index:]:
            if c > best_seen:
                return c == self.maximum  # Success only if it's the best candidate
        return False  # No candidate selected or none better than observed group



if __name__ == "__main__":
    trials = 1000
    n = 100
    r = int(n / 2.71828)  # Optimal stopping index
    successes_list = []
    for r in range(1,100):
        print(r)
        successes = 0
        for _ in range(trials):
            sim = Simulation(n)
            if sim.run(r):
                successes += 1
        successes_list.append(successes)

    print(successes_list.index(max(successes_list)))








