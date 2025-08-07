import random as r
# import matplotlib.pyplot as plt

class Bettor:
    def __init__(self) -> None:
        self.balance: float = 0

    def safe_bet(self) -> float:
        self.balance += 100
        return self.balance
    
    def risky_bet(self) -> float:
        if r.randint(1,1000) == 1:
            pass
        else:
            self.balance += 101
        return self.balance
    
    def get_balance(self) -> float:
        return self.balance
    
if __name__ == "__main__":
    safe_bettor: Bettor = Bettor()
    risky_bettor: Bettor = Bettor()
    SB_rec: list[float] = []
    RB_rec: list[float] = []


    iterations = 1000

    for i in range(iterations):
        SB_rec.append(safe_bettor.safe_bet())
        RB_rec.append(risky_bettor.risky_bet())

    
    

