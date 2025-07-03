'''
This is a game where a fair coin is flipped n times until it lands on heads. When it does
land on heads, you get 2^n dollars as a prize. The game costs money to opt in, so whats the most
would you opt in to play?
'''

import random as r
import statistics

class Coin:
    def __init__(self) -> None:
        self.total_flips = 0
        self.history: list[str] = []
        self.last_toss = None

    def toss(self) -> str:
        faces: list[str] = ["Heads", "Tails"]
        face: str = r.choice(faces)
        self.total_flips += 1
        self.history.append(face)
        self.last_toss = face
        return face
    
    def get_last_toss(self) -> str|None:
        return self.last_toss
    
    
class CoinTossGame:
    def __init__(self) -> None:
        self.coin: Coin = Coin()
        self.prize: int = 2

    def play_game(self) -> int:
        iterations: int = 0
        while self.coin.get_last_toss() != "Heads":
            iterations += 1
            self.coin.toss()
        self.prize = self.prize**iterations
        return self.prize



if __name__ == "__main__":
    record: list[int] = []
    iterations = 1000000
    for i in range(iterations):
        if i % (iterations/100) == 0:
            print(f"{100*i/(iterations)}%")
        game = CoinTossGame()
        record.append(game.play_game())

    print(f'''
        Statistics over {iterations} games:
        -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
        Average win : $ {round(sum(record)/len(record),3)}
        Median win : $ {round(statistics.median(record),3)}
        Biggest win : $ {round(max(record),3)}
        ------
        Odds of winning $8 or less : {round(100*len([r for r in record if r <=  8])/iterations,3)}%
        Odds of winning $16 or less : {round(100*len([r for r in record if r <=  16])/iterations,3)}%
        Odds of winning $32 or less : {round(100*len([r for r in record if r <=  32])/iterations,3)}%
        Odds of winning $64 or less : {round(100*len([r for r in record if r <=  64])/iterations,3)}%
        ------  
        Odds of winning more than $1000 : {round(100*len([r for r in record if r >=  1000])/iterations,3)}%
        Odds of winning exactly $2: {round(100*len([r for r in record if r ==  2])/iterations,3)}%
        ------
        Chance of winning money if you bet $2 : {round(100*len([r for r in record if r >  2])/iterations,3)}%
        Chance of winning money if you bet $4 : {round(100*len([r for r in record if r >  4])/iterations,3)}%
        Chance of winning money if you bet $6 : {round(100*len([r for r in record if r >  6])/iterations,3)}%
        Chance of winning money if you bet $8 : {round(100*len([r for r in record if r >  8])/iterations,3)}%
        Chance of winning money if you bet $10 : {round(100*len([r for r in record if r >  10])/iterations,3)}%
        Chance of winning money if you bet $20 : {round(100*len([r for r in record if r >  20])/iterations,3)}%
        
        ------
        Average win (any events < 0.01% chance cut out) : $ {round(sum([r for r in record if r < 8192])/len([r for r in record if r < 128]),3)}
        ------
        Average profit with $1 bet (any events < 0.01% chance cut out) : $ {round(sum([r for r in record if r < 8192])/len([r for r in record if r < 128]),3)-1}
        Average profit with $2 bet (any events < 0.01% chance cut out) : $ {round(sum([r for r in record if r < 8192])/len([r for r in record if r < 128]),3)-2}
        Average profit with $3 bet (any events < 0.01% chance cut out) : $ {round(sum([r for r in record if r < 8192])/len([r for r in record if r < 128]),3)-3}
        Average profit with $4 bet (any events < 0.01% chance cut out) : $ {round(sum([r for r in record if r < 8192])/len([r for r in record if r < 128]),3)-4}
        Average profit with $5 bet (any events < 0.01% chance cut out) : $ {round(sum([r for r in record if r < 8192])/len([r for r in record if r < 128]),3)-5}
        Average profit with $6 bet (any events < 0.01% chance cut out) : $ {round(sum([r for r in record if r < 8192])/len([r for r in record if r < 128]),3)-6}
        Average profit with $7 bet (any events < 0.01% chance cut out) : $ {round(sum([r for r in record if r < 8192])/len([r for r in record if r < 128]),3)-7}
        Average profit with $8 bet (any events < 0.01% chance cut out) : $ {round(sum([r for r in record if r < 8192])/len([r for r in record if r < 128]),3)-8}
        Average profit with $9 bet (any events < 0.01% chance cut out) : $ {round(sum([r for r in record if r < 8192])/len([r for r in record if r < 128]),3)-9}
        Average profit with $20 bet (any events < 0.01% chance cut out) : $ {round(sum([r for r in record if r < 8192])/len([r for r in record if r < 128]),3)-20}
        -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*        
          ''')
    
    
    
