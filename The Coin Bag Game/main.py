"""
Premise:
----------
You're playing a game where there's two identical bags in front of you that either contains $10 dollars or $100 dollars.
You don't know which is which.

The game-master allows you to pick one bag at random and look at its value. Then, he gives you the chance to swap.
In another twist, if you choose to swap, you can choose to swap again, but with a new bag that is either
10x the value of your current bag or 1/10 the value of your current bag. Should you take this swap, the same
opportunity repeats 100 times, allowing you to swap for a total of 100 times.

Whenever you stop swapping, you get whatever money is in the current sh

What's the logical way to play?
"""
import random as r
import matplotlib.pyplot

class Player:
    def __init__(self, name):
        self.name = name
        self.current_bag = r.choice([10,100])
        self.swaps = 0
        self.record = [self.current_bag]

    def swap(self):
        if self.swaps > 100:
            print(f"no swap performed for player: {self.name}, no swaps left!")
            return
        new_bag = r.choice([self.current_bag*10,self.current_bag*1/10])
        self.current_bag = new_bag
        self.record.append(self.current_bag)
        self.swaps += 1




if __name__ == "__main__":
    iterations = 1000 # for repeatable results

    player_1_results_over_time = []
    player_2_results_over_time = []
    player_3_results_over_time = []
    player_4_results_over_time = []

    for i in range(iterations):
        player_1 = Player("never swap")
        player_2 = Player("conservative wait")  # waits until he has $10_000, then stops
        player_3 = Player("optimistic wait")  # waits until he has $1_000_000, then stops
        player_4 = Player("swap until done")  # swaps every single round

        player_1_results_over_time.append(player_1.current_bag)

        while player_2.current_bag < 10000 and player_2.swaps <= 100:
            player_2.swap()
        player_2_results_over_time.append(player_2.current_bag)

        while player_3.current_bag < 1000000 and player_3.swaps <= 100:
            player_3.swap()
        player_3_results_over_time.append(player_3.current_bag)

        for i in range(100):
            player_4.swap()
        player_4_results_over_time.append(player_4.current_bag)


    print(f"Player 1 results: {sum(player_1_results_over_time)/len(player_1_results_over_time):.2f}")
    print(f"Player 2 results: {sum(player_2_results_over_time) / len(player_2_results_over_time):.2f}")
    print(f"Player 3 results: {sum(player_3_results_over_time) / len(player_3_results_over_time):.2f}")
    print(f"Player 4 results: {sum(player_4_results_over_time) / len(player_4_results_over_time):.2f}")

    print("----------------------------------------------------------------------------------------")

    print(f"Player 1 chance of break-even or better:{len([val for val in player_1_results_over_time if val > 100])/len(player_1_results_over_time):.2f} ")
    print(f"Player 2 chance of break-even or better:{len([val for val in player_2_results_over_time if val > 100])/len(player_2_results_over_time):.2f} ")
    print(f"Player 3 chance of break-even or better:{len([val for val in player_3_results_over_time if val > 100])/len(player_3_results_over_time):.2f} ")
    print(f"Player 4 chance of break-even or better:{len([val for val in player_4_results_over_time if val > 100])/len(player_4_results_over_time):.2f} ")








