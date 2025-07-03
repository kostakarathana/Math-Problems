import random as r


class RouletteWheel:
    def __init__(self) -> None:
        pass

    def spin_and_get_result(self) -> bool:
        '''
        general idea: chance of hitting red is 47.4% on american
        roulette, so just generate a randint[1,1000] and if its 474 or below, 
        you win
        '''
        return r.randint(1,1000) <= 474
    
class Player:
    def __init__(self, infinite_bankroll: bool = False, initial_balance: int = 100) -> None:
        self.infinite_bankroll = infinite_bankroll
        self.roulette_wheel = RouletteWheel()
        self.balance = initial_balance
        self.broke = False
        self.balance_record: list[int] = [self.balance]

    def get_balance(self) -> int:
        return self.balance
    
    def get_is_broke(self) -> bool:
        return self.broke
    
    def bet_on_red(self, amt: int) -> None:
        if not self.infinite_bankroll and (amt > self.balance or self.broke):
            raise ValueError("you can't bet more than you have!")
        
        if self.roulette_wheel.spin_and_get_result():
            self.balance += amt
        else:
            self.balance -= amt
            if self.balance == 0 and not self.infinite_bankroll:
                self.broke = True
        self.balance_record.append(self.balance)
        
    def get_record(self) -> list[int]:
        return self.balance_record

