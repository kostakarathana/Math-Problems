import pygame
import random
import math
from dataclasses import dataclass

# ---------- Tunable parameters ----------
WIDTH, HEIGHT = 1000, 1000
N_AGENTS = 200
INIT_INFECTED = 3
AGENT_SIZE = 6                     # radius for drawing & collision
SPEED_MIN, SPEED_MAX = 1.5, 2.8    # pixels per frame
INFECTION_RADIUS = 2 * AGENT_SIZE  # proximity for infection
INFECTION_PROB = 0.05            # chance to infect on close contact per tick
RECOVERY_TIME = 8 * 60             # frames until outcome (~8s at 60 FPS)
MORTALITY_PROB = 1              # chance an infected dies instead of recovers
FPS = 60

# Colors
HEALTHY_COLOR = (40, 200, 120)
INFECTED_COLOR = (220, 60, 60)
RECOVERED_COLOR = (60, 120, 220)
DEAD_COLOR = (220, 220, 220)
BG = (10, 10, 10)
HUD = (220, 60, 60)

# ---------- State ----------
HEALTHY, INFECTED, RECOVERED, DEAD = range(4)

@dataclass
class Sprite:
    x: float
    y: float
    width: int
    height: int
    color: tuple

    def __post_init__(self):
        # Keep your speed idea, but allow direction
        self.speed = random.uniform(SPEED_MIN, SPEED_MAX)
        angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(angle) * self.speed
        self.vy = math.sin(angle) * self.speed

        self.state = HEALTHY
        self.infection_timer = 0

    @property
    def r(self):
        return self.width // 2  # treat width as diameter in this setup

    def infect(self):
        if self.state == HEALTHY:
            self.state = INFECTED
            self.infection_timer = 0

    def step_disease(self):
        if self.state == INFECTED:
            self.infection_timer += 1
            if self.infection_timer >= RECOVERY_TIME:
                # Outcome roll
                if random.random() < MORTALITY_PROB:
                    self.state = DEAD
                    self.vx = 0
                    self.vy = 0
                else:
                    self.state = RECOVERED

    def move(self):
        if self.state == DEAD:
            return
        self.x += self.vx
        self.y += self.vy

        # Bounce off walls
        if self.x - self.r < 0:
            self.x = self.r
            self.vx = -self.vx
        elif self.x + self.r > WIDTH:
            self.x = WIDTH - self.r
            self.vx = -self.vx

        if self.y - self.r < 0:
            self.y = self.r
            self.vy = -self.vy
        elif self.y + self.r > HEIGHT:
            self.y = HEIGHT - self.r
            self.vy = -self.vy

    def draw(self, surface):
        if self.state == HEALTHY:
            color = HEALTHY_COLOR
        elif self.state == INFECTED:
            color = INFECTED_COLOR
            self.speed = 0.1*self.speed
        elif self.state == RECOVERED:
            color = RECOVERED_COLOR
            self.speed = 2 * self.speed
        else:
            color = DEAD_COLOR
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.r)

def distance_sq(a: Sprite, b: Sprite) -> float:
    dx = a.x - b.x
    dy = a.y - b.y
    return dx * dx + dy * dy

def maybe_infect(a: Sprite, b: Sprite):
    # If either is infected and the other is healthy, infection can spread on proximity
    close = distance_sq(a, b) <= (INFECTION_RADIUS * INFECTION_RADIUS)
    if not close:
        return
    # Attempt infections in both directions (symmetrical)
    if a.state == INFECTED and b.state == HEALTHY and random.random() < INFECTION_PROB:
        b.infect()
    if b.state == INFECTED and a.state == HEALTHY and random.random() < INFECTION_PROB:
        a.infect()

def spawn_agents(n):
    agents = []
    for _ in range(n):
        # Avoid spawning at edges
        x = random.uniform(AGENT_SIZE + 5, WIDTH - AGENT_SIZE - 5)
        y = random.uniform(AGENT_SIZE + 5, HEIGHT - AGENT_SIZE - 5)
        spr = Sprite(x=x, y=y, width=AGENT_SIZE * 2, height=AGENT_SIZE * 2, color=HEALTHY_COLOR)
        agents.append(spr)
    # Seed infections
    for spr in random.sample(agents, k=min(INIT_INFECTED, len(agents))):
        spr.infect()
    return agents

def count_states(agents):
    h = sum(1 for a in agents if a.state == HEALTHY)
    i = sum(1 for a in agents if a.state == INFECTED)
    r = sum(1 for a in agents if a.state == RECOVERED)
    d = sum(1 for a in agents if a.state == DEAD)
    return h, i, r, d

def draw_hud(screen, font, frame, agents):
    h, i, r, d = count_states(agents)
    text = f"n: {h+i+r+d} H:{h} I:{i} R:{r} D:{d} IP: {100-round(100*(h+d+r)/(h+i+r+d),1)} SP: {round(100*(h+i+r)/(h+i+r+d),1)}    t={frame//FPS}s"
    surf = font.render(text, True, HUD)
    screen.blit(surf, (10, 10)) # 200 in 400m2

def main():
    pygame.init()
    pygame.display.set_caption("Disease Spread Simulation (Pygame)")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Menlo", 18)

    agents = spawn_agents(N_AGENTS)

    running = True
    paused = False
    frame = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    agents = spawn_agents(N_AGENTS)
                    frame = 0
                    paused = False

        if not paused:
            # Movement
            for a in agents:
                a.move()

            # Infections (O(n^2) – fine for ~ few hundred agents; you can grid-partition later)
            for i in range(len(agents)):
                ai = agents[i]
                for j in range(i + 1, len(agents)):
                    aj = agents[j]
                    maybe_infect(ai, aj)

            # Disease progression
            for a in agents:
                a.step_disease()

            frame += 1

        # Draw
        screen.fill(BG)
        for a in agents:
            a.draw(screen)
        draw_hud(screen, font, frame, agents)

        # Pause banner
        if paused:
            banner = font.render("PAUSED - SPACE to resume | R to restart | Q/Esc to quit", True, HUD)
            screen.blit(banner, (10, HEIGHT - 30))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()