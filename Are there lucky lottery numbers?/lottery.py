import random as r


class OzLotto:
    def __init__(self) -> None:
        self.num_balls: int = 7
        self.setup()

    def setup(self) -> None: 
        self.balls: list[int] = [r.randint(1,47) for _ in range(self.num_balls)]
    
    def get_results(self, print_on: bool=False) -> list[int]:
        if print_on:
            print(self.balls)
        return self.balls



