import random as r
import matplotlib.pyplot as plt
import numpy as np
import math


class DrunkShooter:
    def __init__(self) -> None:
        self.target_record: list[list[float]] = [[0,0]]
        self.current_x: float = 0
        self.current_y: float = 0
        self.shots_taken: float = 1 # bullseye counts
        
    
    def take_shot_on_last_hole(self) -> None:
        random_change_x: float = r.gauss(0, 1)
        random_change_y: float = r.gauss(0, 1)
        self.current_x += random_change_x
        self.current_y += random_change_y
        self.target_record.append([self.current_x,self.current_y])
    
    def take_shot_randomly(self) -> None:
        random_change_x: float = r.gauss(0, 1)
        random_change_y: float = r.gauss(0, 1)
        random_coordinate: list[float] = r.choice(self.target_record)
        self.current_x = random_coordinate[0]
        self.current_y = random_coordinate[1]
        self.current_x += random_change_x
        self.current_y += random_change_y
        self.target_record.append([self.current_x,self.current_y])

    def take_shot_centroid(self) -> None:
        random_change_x: float = r.gauss(0, 1)
        random_change_y: float = r.gauss(0, 1)
        av_x: list[float] = sum([x[0] for x in self.target_record])/len(self.target_record) # this is so ineffecient for large n but whatever
        av_y: list[float] = sum([y[1] for y in self.target_record])/len(self.target_record)

        self.current_x = av_x
        self.current_y = av_y
        
        self.current_x += random_change_x
        self.current_y += random_change_y
        self.target_record.append([self.current_x,self.current_y])
        self.shots_taken += 1



if __name__ == "__main__":
    shooter = DrunkShooter()
    shots_taken = 100000

    for i in range(shots_taken):
        shooter.take_shot_centroid()
    
    x = [x[0] for x in shooter.target_record]
    y = [y[1] for y in shooter.target_record]
    
    num_points = len(x)
    colors = plt.cm.plasma(np.linspace(0, 1, num_points))  # smooth gradient

    # Plot all shots with gradient color
    plt.scatter(x, y, c=colors, marker="x", cmap='plasma')

    # Highlight (0, 0) as bold black circle
    plt.scatter(0, 0, s=100, color='black', label='Origin (0,0)', zorder=5)

    # Balanced axis: calculate max range
    max_range = max(
        max(abs(min(x)), abs(max(x))),
        max(abs(min(y)), abs(max(y)))
    )
    max_range*=1.1

    plt.xlim(-max_range, max_range)
    plt.ylim(-max_range, max_range)

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.title("Drunk Shooter: Shot Dispersion Over Time")
    plt.legend()
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')  # Equal scaling
    plt.show()
        
    
        

