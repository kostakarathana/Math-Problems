import matplotlib.pyplot as plt
from game import Game
import numpy as np


if __name__ == "__main__":
    
    record: list[float] = []

    iterations = 100000
    bet_perc = 25
    for _ in range(iterations):
        game: Game = Game()
        while game.get_game_status():
            game.play_round(bet_perc)
        record.append(game.get_cash())



    average = round(sum(record)/len(record),3)
    winning_perc = round(100*(len([r for r in record if r > 100])/len(record)),3)

    bins = np.linspace(min(record), max(record), 30)





    # plt.figure(figsize=(12, 6))
    # plt.hist(record, bins=bins, edgecolor='black', width=(bins[1] - bins[0]) * 0.9)  # 10% space between bars
    # plt.title("Distribution of Final Cash After 1000 Games")
    # plt.xlabel("Final Cash")
    # plt.ylabel("Frequency")

    # # Improve x-axis readability
    # plt.xticks(np.round(bins, 2), rotation=45, ha='right')
    # plt.grid(True, linestyle='--', alpha=0.6)
    # plt.tight_layout()
    # plt.show()
            
