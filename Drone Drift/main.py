import random as r
import matplotlib.pyplot as plt
import numpy as np
import math
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class Drone:
    def __init__(self) -> None:
        self.record: list[list[float]] = [[0,0,0]]
        self.current_x: float = 0
        self.current_y: float = 0
        self.current_z: float = 0
        self.moves_made: float = 0
        
    
    def move(self) -> None:
        random_change_x: float = r.gauss(0, 1)
        random_change_y: float = r.gauss(0, 1)
        random_change_z: float = r.gauss(0, 1)

        self.current_x += random_change_x
        self.current_y += random_change_y
        self.current_z += random_change_z

        self.record.append([self.current_x,self.current_y,self.current_z])



if __name__ == "__main__":
    drone = Drone()
    for i in range(100000):
        drone.move()

    x = [point[0] for point in drone.record]
    y = [point[1] for point in drone.record]
    z = [point[2] for point in drone.record]

    # Create a color gradient: older = warmer (red), newer = colder (blue)
    # Normalize so index 0 is red, last is blue
    colors = np.linspace(1, 0, len(drone.record))  # 1 = red (older), 0 = blue (newer)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Use scatter with a colormap (e.g., 'autumn' or reversed 'coolwarm')
    sc = ax.scatter(x, y, z, c=colors, cmap='autumn')  # 'autumn' is red → yellow
    # OR try cmap='coolwarm_r' for blue → red reversed

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Drone Flight Path (Warm to Cold)')

    plt.colorbar(sc, ax=ax, label="Warm (old) → Cold (new)")
    plt.show()
        
    
        

