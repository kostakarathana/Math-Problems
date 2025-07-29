'''
BROKEN AT THE MOMENT
'''


import pygame
import pygame_gui
import random
import time

# Vehicle definitions
class Car:
    def __init__(self, lane, vehicle_type, speed_limit, braking_distance):
        self.lane = lane
        self.type = vehicle_type
        base_speeds = {
            'car': speed_limit,
            'truck': speed_limit * 0.8,
            'bike': speed_limit * 1.1
        }
        self.desired_speed = base_speeds.get(vehicle_type, speed_limit)
        self.speed = self.desired_speed * random.uniform(0.7, 1.0)
        self.braking_distance = braking_distance * random.uniform(0.8, 1.2)
        self.width = 0
        self.length = 0
        self.x = 0

    def update(self, dt, speed_limit, cars_in_lane):
        # look for the car right ahead in this lane
        ahead = [c for c in cars_in_lane if c.x > self.x]
        if ahead:
            gap = min(c.x - self.x for c in ahead)
            if gap < self.braking_distance:
                # brake
                self.speed = max(0, self.speed - 5 * dt)
            else:
                # go to desired/speed limit
                self.speed = min(self.desired_speed, speed_limit)
        else:
            self.speed = min(self.desired_speed, speed_limit)
        self.x += self.speed * dt

class Highway:
    def __init__(self, num_lanes, lane_width, length):
        self.num_lanes = num_lanes
        self.lane_width = lane_width
        self.length = length
        self.cars = []

    def update(self, dt, speed_limit):
        for lane_idx in range(self.num_lanes):
            lane_cars = [c for c in self.cars if c.lane == lane_idx]
            for car in lane_cars:
                car.update(dt, speed_limit, lane_cars)

    def draw(self, surface):
        # draw road and lanes
        for i in range(self.num_lanes + 1):
            y = i * self.lane_width
            pygame.draw.line(surface, (200, 200, 200), (0, y), (self.length, y), 2)
        # draw each vehicle
        for car in self.cars:
            rx = int(car.x)
            ry = int(car.lane * self.lane_width + (self.lane_width - car.width) / 2)
            color = {
                'car': (0, 120, 250),
                'truck': (200, 50, 50),
                'bike': (50, 200, 50)
            }[car.type]
            rect = pygame.Rect(rx, ry, car.length, car.width)
            pygame.draw.rect(surface, color, rect)

def main():
    pygame.init()
    WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Traffic Simulation")
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    # default params
    speed_limit = 100.0        # units/sec
    spawn_rate = 20.0          # vehicles per minute
    braking_distance = 50.0    # units
    lane_width = 80            # px
    num_lanes = 3
    spawn_probs = {'car': 0.6, 'truck': 0.3, 'bike': 0.1}

    # UI setup
    sliders = {}
    labels = {}
    params = [
        ("Speed Limit", 10, 200, speed_limit),
        ("Density (veh/min)", 1, 60, spawn_rate),
        ("Braking Dist", 10, 200, braking_distance),
        ("Lane Width", 40, 160, lane_width),
        ("# Lanes", 1, 6, num_lanes),
    ]
    for idx, (name, mn, mx, val) in enumerate(params):
        y = 10 + idx * 50
        labels[name] = pygame_gui.elements.UILabel(
            pygame.Rect( (10, y), (140, 30) ),
            text=f"{name}: {val}",
            manager=manager
        )
        sliders[name] = pygame_gui.elements.UIHorizontalSlider(
            pygame.Rect((160, y), (200, 30)),
            start_value=val,
            value_range=(mn, mx),
            manager=manager
        )

    highway = Highway(num_lanes, lane_width, length=800)
    exit_times = []

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            manager.process_events(event)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                for name, slider in sliders.items():
                    if event.ui_element == slider:
                        v = int(event.value) if name == "# Lanes" else event.value
                        labels[name].set_text(f"{name}: {v}")
                        if name == "Speed Limit":
                            speed_limit = v
                        elif name == "Density (veh/min)":
                            spawn_rate = v
                        elif name == "Braking Dist":
                            braking_distance = v
                        elif name == "Lane Width":
                            lane_width = v
                        elif name == "# Lanes":
                            num_lanes = v
                            highway = Highway(num_lanes, lane_width, length=800)
                            exit_times.clear()

        manager.update(dt)

        # spawn new vehicles
        if random.random() < (spawn_rate / 60.0) * dt:
            lane = random.randrange(num_lanes)
            r = random.random()
            cum = 0
            for vt, prob in spawn_probs.items():
                cum += prob
                if r < cum:
                    vehicle_type = vt
                    break
            car = Car(lane, vehicle_type, speed_limit, braking_distance)
            car.width = lane_width * 0.6
            car.length = lane_width * 0.4
            highway.cars.append(car)

        highway.update(dt, speed_limit)

        # remove cars past the end
        now = time.time()
        remaining = []
        for c in highway.cars:
            if c.x < highway.length:
                remaining.append(c)
            else:
                exit_times.append(now)
        highway.cars = remaining

        # compute stats
        cpm = sum(1 for t in exit_times if now - t <= 60)
        avg_speed = sum(c.speed for c in highway.cars) / max(len(highway.cars), 1)

        # draw
        screen.fill((30, 30, 30))
        highway.draw(screen)

        # overlay metrics
        font = pygame.font.SysFont(None, 24)
        for i, txt in enumerate([
            f"Throughput: {cpm} veh/min",
            f"Active Vehicles: {len(highway.cars)}",
            f"Avg Speed: {avg_speed:.1f}"
        ]):
            surf = font.render(txt, True, (255,255,255))
            screen.blit(surf, (400, 10 + i*25))

        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()