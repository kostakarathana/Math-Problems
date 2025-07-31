import random as r

class Game:
    def __init__(self, boats: int = 7) -> None:
        self.boats = boats
        self.boat_choices = [i for i in range(1,self.boats+1)]
        self.game_over = False
        self.current_boat = r.choice(self.boat_choices)

        self.record: list[str] = []
        self.detailed_record: list[str] = []

    def jump(self) -> None:
        previous_boat: int = self.current_boat
        self.boat_choices.remove(self.current_boat)
        if self.boats == 1:
            self.game_over = True
            return
        
        self.current_boat = r.choice(self.boat_choices)
        self.detailed_record.append(f"boat {previous_boat} -> boat {self.current_boat}")
        if self.current_boat > previous_boat:
            self.record.append("R")
        else:
            self.record.append("L")
        self.boats -= 1

if __name__ == "__main__":
    simulations = 1000000
    number_of_single_lefts = 0


    for i in range(simulations):
        game = Game(20)
        while not game.game_over:
            game.jump()
        if game.record.count("L") == 1:
            number_of_single_lefts += 1
    print(f"percentage where pirate jumped left exactly once: {number_of_single_lefts*100/simulations}")



    