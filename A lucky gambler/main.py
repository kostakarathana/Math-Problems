from roulette import Player
import matplotlib.pyplot as plt

if __name__ == "__main__":
    players = 1000
    bets_per_iteration: list[int] = [i for i in range(1,101)]
    average_profit_record: list[float] = []


    for i in range(len(bets_per_iteration)):
        total_profit = 0.0
        for j in range(players):
            player = Player(True,0)
            for betamt in range(i + 1):
                player.bet_on_red(100)
            # Use a method to get profit, or replace with the correct attribute if available
            total_profit += player.get_balance()  # Replace with player.profit if that's correct
        average_profit_record.append(total_profit / players)

    plt.plot(average_profit_record)
    plt.show()