"""
Simple game where you start with $100. You can bet $1 on a coin flip, doubling
your money or losing it. You can bet until you either want to stop or have $0.
"""
import random
import matplotlib.pyplot as plt

class Bettor:
    def __init__(self,stop_loss: int = 0, take_profit: int = 10**10):
        self.money = 100
        self.stop_loss = stop_loss
        self.take_profit = take_profit
        self.bets_taken = 0
        self.money_record = []

    def bet(self) -> bool: # returns true if the player can still bet
        if self.money == 0:
            return False
        elif self.money <= self.stop_loss:
            return False
        elif self.money >= self.take_profit:
            return False

        if random.randint(1,2) == 1:
            self.money += 1
        else:
            self.money -= 1
        self.money_record.append(self.money)
        return True

if __name__ == "__main__":

    player1 = Bettor(50,200)
    player2 = Bettor(0,1000)

    while player1.bet():
        continue
    while player2.bet():
        continue

    plt.plot(player1.money_record)
    plt.plot(player2.money_record)
    plt.show()




