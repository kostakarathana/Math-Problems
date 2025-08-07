import random as r

class Bettor:
    def __init__(self) -> None:
        self.balance: int = 0

    def safe_bet(self) -> None:
        self.balance += 100
    
    def risky_bet(self) -> None:
        if r.randint(1,1000) == 1:
            return
        else:
            self.balance += 101
    
    def get_balance(self) -> int:
        return self.balance
    
if __name__ == "__main__":
    safe_bettor = Bettor()
    risky_bettor = Bettor()

    iterations = 1000

    for i in range(iterations):
        safe_bettor.safe_bet()
        risky_bettor.risky_bet()
    
    print(safe_bettor.get_balance())
    print(risky_bettor.get_balance())
