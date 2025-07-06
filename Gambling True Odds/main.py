import random
import matplotlib.pyplot as plt

class RouletteWheel:
    def __init__(self, starting_balance=100, bet_size=10):
        self.balance = starting_balance
        self.starting_balance = starting_balance
        self.bet_size = bet_size

    def spin(self):
        random_num = random.randint(1, 1000)
        if random_num <= 474: # 474 to simulate house edge
            self.balance += self.bet_size
        else:
            self.balance -= self.bet_size

    def get_is_profitable(self):
        return self.balance > self.starting_balance

# Simulation settings
max_rounds = 100
simulations_per_point: int = 100
profitability_by_round = []

for rounds in range(1, max_rounds + 1):
    wheel_bal_av: float = 0.0

    for _ in range(simulations_per_point):
        wheel = RouletteWheel()
        for _ in range(rounds):
            wheel.spin()
        if wheel.get_is_profitable():
            wheel_bal_av += wheel.balance

    profitability = wheel_bal_av
    profitability_by_round.append(profitability)



# Plot
plt.plot(figsize=(12, 6))
plt.plot(range(1, max_rounds + 1), profitability_by_round)
plt.title("Probability of Profit vs. Number of Games Played")
plt.xlabel("Number of Rounds Played")
plt.ylabel("Probability of Being Profitable")
plt.grid(True)
plt.tight_layout()
plt.show()