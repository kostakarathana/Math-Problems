import random as r

class Game:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.drawn = 0
        self.game_over = False

    def draw(self):
        choice = r.randint(0,1)

        if choice == 0:
            self.n -= 1
            self.drawn += 1
        else:
            self.m -= 1
            self.drawn += 1
        if self.n == 0 or self.m == 0:
            self.game_over = True
            return

if __name__ == "__main__":

    results = []
    for i in range(100):
        game = Game(12, 20)
        while game.game_over == False:
            game.draw()
        results.append(game.drawn)
    print(sum(results)/len(results))

