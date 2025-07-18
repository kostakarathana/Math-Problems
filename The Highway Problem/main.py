'''
Problem: What's the optimal speed in km/h for cars to travel
down a highway to get the most cars through every time interval?
'''

import matplotlib.pyplot as plt
import math

class Highway:
    def __init__(self, speed_limit: int, lanes: int = 4) -> None:
        self.speed_limit = speed_limit  # in km/h
        self.lanes = lanes
        self.speed_m_s = self.speed_limit * 1000 / 3600


        # self.braking_distance = 0.00577381*self.speed_limit**2 + 0.385119*self.speed_limit + 1.23214 # dry conservative
        self.braking_distance = 0.00791667*self.speed_limit**2 + 0.430357*self.speed_limit - 0.0892857 # wet conservative
        # self.braking_distance = self.speed_m_s*2 # "two second between" rule of thumb
        # braking_distance = speed_m_s*3 # "three second between" rule of thumb

    def calculate_max_cars(self, time_period_h: float = 1.0) -> int:

        car_length = 4
        total_gap = self.braking_distance + car_length  
        cars_per_second_per_lane = self.speed_m_s / total_gap

        # Total cars over time period across all lanes
        total_seconds = time_period_h * 3600
        total_cars = cars_per_second_per_lane * total_seconds * self.lanes

        return int(round(total_cars))
    
    def get_safety_rating(self) -> float:
        # Roughly Nilssons power model

        x = self.speed_limit
        exponent = -1 * (0.0619719 * x - 5.21318)
        y: float = 100.8366/ (1 + math.exp(exponent))
        return y
    
    def get_braking_distance(self) -> float:
        return self.braking_distance


    

 
if __name__ == "__main__":
    speeds = [v for v in range(10, 501, 10)]
    cars: list[int] = []
    safety: list[float] = []
    braking_distances: list[float] = []

    for v in speeds:
        hw = Highway(speed_limit=v)
        cars.append(hw.calculate_max_cars(1))
        safety.append(hw.get_safety_rating())
        braking_distances.append(hw.get_braking_distance())
    
    print(braking_distances)

    # Plotting
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color1 = 'tab:blue'
    ax1.set_xlabel('Speed (km/h)', fontsize=12)
    ax1.set_ylabel('Max Cars per Hour (4 lanes)', color=color1, fontsize=12)
    ax1.plot(speeds, cars, color=color1, linewidth=2, label='Max Cars per Hour')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    ax2 = ax1.twinx()
    color2 = 'tab:red'
    ax2.set_ylabel('Fatality Risk (%)', color=color2, fontsize=12)
    ax2.plot(speeds, safety, color=color2, linewidth=2, linestyle='--', label='Safety Risk')
    ax2.tick_params(axis='y', labelcolor=color2)

    fig.tight_layout()
    plt.title("Highway Speed vs Max Cars and Fatality Risk", fontsize=14)
    plt.show()