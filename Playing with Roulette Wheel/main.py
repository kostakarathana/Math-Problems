import matplotlib
import random as r

global betting_guide
global betting_payouts
betting_guide: dict[str, str] = {

}




class Bet:
    def __init__(self, amount: int, bet_type: str, player_from):
        self.amount = amount
        self.bet_type = bet_type
        self.player_from = player_from



class Roulette:
    def __init__(self):
        self.slots: list[str] = ["1","2","3","4","5",
                      "6","7","8","9","10",
                      "11","12","13","14","15",
                      "16","17","18","19","20",
                      "21","22","23","24","25","26",
                      "27","28","29","30","31","32",
                      "33","34","35","36","0","00"]
        self.special_bets: list[str] = ["Even", "Odd", "Red", "Black",
                                        "Dozen_1","Dozen_2","Dozen_3",
                                        "Row_1","Row_2","Row_3"]

        self.history: list[str] = []
        self.current_bets: list[Bet] = []

    def take_bet(self, bet: Bet) -> None:
        self.current_bets.index(bet)


    def spin(self) -> str:
        slot: str = r.choice(self.slots)
        self.history.append(slot)
        for bet in self.current_bets:
            if bet.bet_type == "Odd":
        return slot


class Player:
    def __init__(self, name:str):
        self.capital = 10000
        self.name = name

     def place_bet(self, wheel: Roulette, amount: int, bet_type: str) -> None:
         if amount > self.capital:
             print(f"player {self.name} cannot make this bet")
             return
         if bet_type not in wheel.slots or bet_type not in wheel.special_bets:
             print(f"invalid bet  for {self.name}")
             return

         bet = Bet(amount, bet_type, self)
         wheel.take_bet(bet)



