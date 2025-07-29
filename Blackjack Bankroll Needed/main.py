import random as r
import matplotlib.pyplot as plt

class CardCountingBlackJackGame:
    def __init__(self, edge_percentage: int, bankroll: int = 200) -> None:
        self.bankroll = bankroll
        self.edge_percentage = edge_percentage
    
    def play(self, bet: int = 20) -> None:
        win_odds: float = 0.5 + self.edge_percentage/200
        win: bool = True if r.random() <= win_odds else False

        if win:
            self.bankroll += bet
        else:
            self.bankroll -= bet
        
if __name__ == "__main__":
    

    games_per_player = 100
    players = 10000
    recorded_final_bankroll: list[int]= []
    starting_bankroll = 200

    for j in range(players):
        game = CardCountingBlackJackGame(1,starting_bankroll)
        broke = False
        for i in range(games_per_player):
            game.play()
            if game.bankroll <= 0:
                recorded_final_bankroll.append(-1)
                broke = True
                break
        if not broke:
            recorded_final_bankroll.append(game.bankroll)
        
        
    profitability = len([val for val in recorded_final_bankroll if val > starting_bankroll])/players
    print(profitability)

        

    

