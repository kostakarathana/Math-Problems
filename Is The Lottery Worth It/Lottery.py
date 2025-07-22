import random as r

class PowerballLotto:
    def __init__(self) -> None:
        self.balance = 500
        self.jackpot_odds = 134490400

    def play(self) -> bool:
        self.balance -= 28
        number = r.randint(1,self.jackpot_odds)
        if number == 1:
            return True
        return False
    
    def expected_value(self) -> float:
        return + 200_000_000*(1/self.jackpot_odds)
    

    
    
        
        

if __name__ == "__main__":
    
    lotto = PowerballLotto()
    print(lotto.expected_value())

    # definitely not worth it!!!!!