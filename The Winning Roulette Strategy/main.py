import random

class RouletteWheel:
    def __init__(self) -> None:
        self.records: list[bool] = []

    def spin(self, bet:float) -> float:
        random_num = random.randint(1, 1000)
        if random_num <= 474: # 474 to simulate house edge
            self.records.append(True)
            return bet
        else:
            self.records.append(False)
            return -bet


if __name__ == "__main__":
    wheel = RouletteWheel()
    initial_balance: float = 500
    balance: float = initial_balance
    current_bet: float= 20
    cash_spent: float = 0
    
    iterations_taken = 0

    while initial_balance >= balance:
        # if balance < 0 or balance-current_bet < 0:
        #     raise ValueError("out of money!")
        
        balance += wheel.spin(current_bet)
        current_bet *= 2
        iterations_taken += 1
        cash_spent += current_bet
    

    print(f'''
    iterations taken: {iterations_taken}
    cash spent: {cash_spent}
    starting cash: {initial_balance}
    final cash: {balance}
    ''')

    

    


