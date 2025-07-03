import random as r

class Game:
    def __init__(self) -> None:
        self.games_left: int = 100
        self.cash: float = 100

    def play_round(self, perc: float) -> None:
        if self.cash == 0:
            perc = 0
        if perc < 0 or perc > 100:
            raise ValueError(f"you can't bet {perc}%, has to be 0% -> 100%")
        
        bet = self.cash * (perc / 100)
        toss = r.choice(['H','T'])
        if toss == 'H':
            self.cash += bet*2
        else:
            self.cash -= bet
        self.games_left -= 1

    def get_cash(self) -> float:
        return self.cash
    
    def get_game_status(self) -> bool:
        if self.games_left > 0:
            return True
        return False








