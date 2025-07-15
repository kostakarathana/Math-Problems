import random as r
import matplotlib.pyplot as plt

class DartBoard:
    def __init__(self) -> None:
        self.number_inside_unit_circle: int = 0
        self.darts_thrown: int = 0
    
    def throw_dart(self) -> None:
        x = r.uniform(-1, 1)
        y = r.uniform(-1, 1)
        self.darts_thrown += 1
        if x**2 + y**2 <= 1:
            self.number_inside_unit_circle += 1
    
    def estimate_pi(self) -> float:
        return 4*(self.number_inside_unit_circle/self.darts_thrown)
    

if __name__ == "__main__":
    board = DartBoard()
    estimations = []

    for i in range(2,10000000):
        board.throw_dart()
        if i % 1000 == 0:
            estimations.append(board.estimate_pi())
        
    plt.plot(estimations)
    plt.axhline(y=3.141592653589793, color='r', linestyle='--', label='π')
    plt.legend()
    plt.show()

    

