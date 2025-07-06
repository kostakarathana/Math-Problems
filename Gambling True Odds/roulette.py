import random as r


class RouletteWheel:
    def __init__(self, starting_balance=100, bet_size=10):
        self.balance = starting_balance
        self.starting_balance = starting_balance
        self.bet_size = bet_size

    def spin(self) -> None:
        # 47.4% win chance for red in American roulette
        if r.randint(1, 1000) <= 474:
            self.balance += self.bet_size
        else:
            self.balance -= self.bet_size

    def get_is_profitable(self) -> bool:
        return self.balance > self.starting_balance