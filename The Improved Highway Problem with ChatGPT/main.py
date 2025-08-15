import pygame
import random
import math
from collections import deque

# -----------------------------
# Config
# -----------------------------
LANES = 3
HIGHWAY_LENGTH_M = 10_000  # 10 km
EXITS_M = [2_000, 4_000, 6_000, 8_000, 10_000]  # 5 exits
EXIT_MERGE_START = 1_000   # start trying to be in rightmost lane this far before exit
LANE_HEIGHT_PX = 48
MARGIN_PX = 24

# Render scale: 10,000 m -> 1600 px (fits most screens nicely)
PX_PER_M = 1600 / HIGHWAY_LENGTH_M
SCREEN_W = int(HIGHWAY_LENGTH_M * PX_PER_M) + 2 * MARGIN_PX
SCREEN_H = LANE_HEIGHT_PX * LANES + 2 * MARGIN_PX

FPS = 60
DT = 0.2  # seconds per sim step (simulation updates every frame)

# Spawning
INITIAL_SPAWN_RATE = 0.6  # cars per second; bump to see congestion emerge

# Vehicle parameters (simple)
MIN_SPEED = 5.0      # m/s (18 km/h)
MAX_SPEED = 42.0     # m/s (151 km/h)
DEFAULT_DESIRED_SPEED = 33.0  # m/s (~119 km/h)
MAX_ACCEL = 2.0      # m/s^2
MAX_DECEL = 4.5      # m/s^2 (comfortable-ish emergency)
CAR_LENGTH_M = 4.5
CAR_WIDTH_PX = int(LANE_HEIGHT_PX * 0.6)
SAFE_TIME_HEADWAY = 1.2  # seconds
MIN_GAP = 4.0  # meters (buffer)
LANE_CHANGE_LOOK_BACK = 12.0  # need this much gap behind to enter
LANE_CHANGE_LOOK_AHEAD = 18.0 # need this much gap ahead to enter
LANE_CHANGE_COOLDOWN = 2.0    # seconds between lane changes

# Colors
BG = (8, 10, 14)
LANE_COLOR = (40, 44, 52)
EXIT_COLOR = (90, 90, 90)
CAR_COLOR = (80, 180, 255)
SLOW_COLOR = (255, 120, 120)
FAST_COLOR = (120, 255, 160)
TEXT = (220, 220, 220)


class Car:
    __slots__ = ("x", "v", "a", "lane", "desired_speed", "exit_pos", "time_since_lane_change", "will_exit_here")

    def __init__(self, v0: float, lane: int, exit_pos: float):
        self.x = 0.0                   # meters from start
        self.v = max(MIN_SPEED, min(v0, MAX_SPEED))
        self.a = 0.0
        self.lane = lane
        self.desired_speed = v0
        self.exit_pos = exit_pos
        self.time_since_lane_change = LANE_CHANGE_COOLDOWN
        self.will_exit_here = False

    def rect(self):
        # Visual rectangle representing the car
        y_top = MARGIN_PX + self.lane * LANE_HEIGHT_PX + 6
        w = max(6, int(CAR_LENGTH_M * PX_PER_M))
        h = LANE_HEIGHT_PX - 12
        x_px = MARGIN_PX + int(self.x * PX_PER_M)
        return pygame.Rect(x_px - w // 2, y_top, w, h)


class Highway:
    def __init__(self):
        self.cars: list[Car] = []
        self.spawn_accumulator = 0.0
        self.spawn_rate = INITIAL_SPAWN_RATE  # cars/sec
        self.paused = False
        self.show_velocity_colors = True
        self.time = 0.0
        self.spawn_id = 0

    # --------- Spawning / Removal ----------
    def spawn_car(self):
        # Random desired speed with some heterogeneity, and occasional "truck" slow vehicles
        if random.random() < 0.15:
            v0 = random.uniform(20.0, 27.0)  # trucks
        else:
            v0 = random.gauss(DEFAULT_DESIRED_SPEED, 4.0)
            v0 = max(MIN_SPEED, min(v0, MAX_SPEED))
        lane = random.randint(0, LANES - 1)
        exit_pos = random.choice(EXITS_M)
        c = Car(v0=v0, lane=lane, exit_pos=exit_pos)

        # Try to avoid immediate collisions at spawn: ensure a gap in chosen lane
        lane_cars = [car for car in self.cars if car.lane == lane and car.x < 120.0]
        if lane_cars:
            nearest = min((120.0 - car.x) for car in lane_cars)
            if nearest < (CAR_LENGTH_M + 2.0):
                return  # skip this tick; no room

        self.cars.append(c)
        self.spawn_id += 1

    def remove_exited_or_finished(self):
        # Remove cars that took their exit (must be in rightmost lane) or reached end
        survivors = []
        for c in self.cars:
            took_exit = (c.lane == LANES - 1) and (c.x >= c.exit_pos)
            reached_end = c.x >= HIGHWAY_LENGTH_M
            if not (took_exit or reached_end):
                survivors.append(c)
        self.cars = survivors

    # --------- Neighborhood Queries ----------
    def get_front_car(self, lane, x):
        # Return front car in the same lane ahead of position x (smallest positive headway)
        front = None
        best_d = 1e9
        for c in self.cars:
            if c.lane == lane and c.x > x:
                d = c.x - x
                if d < best_d:
                    best_d = d
                    front = c
        return front, best_d

    def get_back_car(self, lane, x):
        # Car behind (largest negative headway)
        back = None
        best_d = -1e9
        for c in self.cars:
            if c.lane == lane and c.x < x:
                d = x - c.x
                if d < (x - (back.x if back else -1e9)):
                    back = c
        if back is None:
            return None, 1e9
        return back, (x - back.x)

    # --------- Dynamics ----------
    def desired_accel(self, c: Car):
        # Very simple car-following: try to reach desired speed; brake if front-gap too small
        front, gap = self.get_front_car(c.lane, c.x)
        # Safe gap target based on current speed
        desired_gap = max(MIN_GAP, c.v * SAFE_TIME_HEADWAY + CAR_LENGTH_M)
        accel = MAX_ACCEL * (1.0 - c.v / max(1e-3, c.desired_speed))
        if front:
            # If we are too close, apply braking proportional to deficit
            if gap < desired_gap:
                # brake harder the closer we are
                deficit = (desired_gap - gap) / max(desired_gap, 1.0)
                accel -= MAX_DECEL * (0.5 + 1.5 * deficit)
        return max(-MAX_DECEL, min(MAX_ACCEL, accel))

    def lane_change_decision(self, c: Car):
        # Try to change lanes if: (1) need to exit soon -> move right,
        # or (2) stuck behind slow car and neighbor lane has better gaps.
        c.time_since_lane_change += DT
        if c.time_since_lane_change < LANE_CHANGE_COOLDOWN:
            return  # on cooldown

        need_exit = (c.exit_pos - c.x) <= EXIT_MERGE_START
        target_dir = None

        # If we need to exit, bias towards moving right (to rightmost lane index LANES-1)
        if need_exit and c.lane < (LANES - 1):
            target_dir = +1  # move right
        else:
            # Otherwise, consider passing: if big slowdown ahead, try the better side
            front, gap = self.get_front_car(c.lane, c.x)
            stuck = (front is not None) and (gap < (c.v * SAFE_TIME_HEADWAY * 0.9))
            if stuck:
                # choose side with more room; try left first (if exists), then right
                candidates = []
                if c.lane > 0:
                    candidates.append(-1)
                if c.lane < LANES - 1:
                    candidates.append(+1)

                best_side = None
                best_room = -1.0
                for d in candidates:
                    lane2 = c.lane + d
                    f2, gap_ahead = self.get_front_car(lane2, c.x)
                    b2, gap_behind = self.get_back_car(lane2, c.x)
                    room = min(gap_ahead if gap_ahead else 1e9, gap_behind if gap_behind else 1e9)
                    if room > best_room:
                        best_room = room
                        best_side = d
                target_dir = best_side

        if target_dir is None:
            return

        lane2 = c.lane + target_dir
        if lane2 < 0 or lane2 >= LANES:
            return

        # Safety check: need gaps ahead/behind in the target lane
        f2, gap_ahead = self.get_front_car(lane2, c.x)
        b2, gap_behind = self.get_back_car(lane2, c.x)
        need_ahead = max(LANE_CHANGE_LOOK_AHEAD, c.v * 0.6)
        need_behind = max(LANE_CHANGE_LOOK_BACK, (b2.v if b2 else 0.0) * 0.5)

        if gap_ahead >= need_ahead and gap_behind >= need_behind:
            c.lane = lane2
            c.time_since_lane_change = 0.0

    def step(self):
        if self.paused:
            return

        # Spawn Poisson-like: accumulate expected spawns
        self.spawn_accumulator += self.spawn_rate * DT
        while self.spawn_accumulator >= 1.0:
            self.spawn_car()
            self.spawn_accumulator -= 1.0

        # Update kinematics
        for c in self.cars:
            # If approaching exit and not yet in rightmost lane, mark intent
            c.will_exit_here = (c.exit_pos - c.x) <= EXIT_MERGE_START

            # Lane change decision before speed update (greedy)
            self.lane_change_decision(c)

        for c in self.cars:
            c.a = self.desired_accel(c)
            c.v = max(MIN_SPEED * 0.25, min(MAX_SPEED, c.v + c.a * DT))
            c.x += c.v * DT

        # Remove cars that have exited or reached the end
        self.remove_exited_or_finished()
        self.time += DT

    # --------- Rendering ----------
    def draw(self, surf: pygame.Surface, font):
        surf.fill(BG)

        # Lanes
        for i in range(LANES):
            y = MARGIN_PX + i * LANE_HEIGHT_PX
            pygame.draw.rect(surf, LANE_COLOR, (MARGIN_PX, y, SCREEN_W - 2 * MARGIN_PX, LANE_HEIGHT_PX), border_radius=10)

        # Exits (draw dashed vertical markers, and a "merge" triangle into rightmost lane)
        for ex in EXITS_M:
            x_px = MARGIN_PX + int(ex * PX_PER_M)
            pygame.draw.line(surf, EXIT_COLOR, (x_px, MARGIN_PX), (x_px, SCREEN_H - MARGIN_PX), 2)
            # shaded merge region for last 1 km before exit on rightmost lane
            x0 = MARGIN_PX + int(max(0, (ex - EXIT_MERGE_START)) * PX_PER_M)
            y_top = MARGIN_PX + (LANES - 1) * LANE_HEIGHT_PX
            pygame.draw.polygon(surf, (30, 30, 35),
                                [(x0, y_top),
                                 (x_px, y_top),
                                 (x_px, y_top + LANE_HEIGHT_PX)],
                                0)

        # Cars
        for c in self.cars:
            r = c.rect()
            if self.show_velocity_colors:
                t = (c.v - 10.0) / (MAX_SPEED - 10.0)
                t = max(0.0, min(1.0, t))
                col = (
                    int(SLOW_COLOR[0] * (1 - t) + FAST_COLOR[0] * t),
                    int(SLOW_COLOR[1] * (1 - t) + FAST_COLOR[1] * t),
                    int(SLOW_COLOR[2] * (1 - t) + FAST_COLOR[2] * t),
                )
            else:
                col = CAR_COLOR
            pygame.draw.rect(surf, col, r, border_radius=6)
            # small exit-intent notch on right side
            if c.will_exit_here and c.lane != (LANES - 1):
                pygame.draw.rect(surf, (230, 230, 60), (r.right - 4, r.centery - 4, 4, 8))

        # HUD
        hud_lines = [
            f"t = {self.time:6.1f}s",
            f"cars = {len(self.cars)}",
            f"spawn = {self.spawn_rate:.2f} cars/s  ([ / ] to change)",
            "P pause | R reset | V velocity colors | ESC quit",
        ]
        y = 6
        for line in hud_lines:
            txt = font.render(line, True, TEXT)
            surf.blit(txt, (8, y))
            y += txt.get_height() + 2


def reset_world():
    return Highway()


def main():
    pygame.init()
    pygame.display.set_caption("Highway Traffic Emergence (10 km, 5 exits)")
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 16)

    world = reset_world()

    running = True
    while running:
        # --- Input ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_p:
                    world.paused = not world.paused
                elif event.key == pygame.K_r:
                    world = reset_world()
                elif event.key == pygame.K_LEFTBRACKET:  # [
                    world.spawn_rate = max(0.0, world.spawn_rate - 0.1)
                elif event.key == pygame.K_RIGHTBRACKET:  # ]
                    world.spawn_rate = min(5.0, world.spawn_rate + 0.1)
                elif event.key == pygame.K_v:
                    world.show_velocity_colors = not world.show_velocity_colors

        # --- Update ---
        world.step()

        # --- Render ---
        world.draw(screen, font)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()