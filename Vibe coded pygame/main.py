import pygame
import random
import math
import json
import os
from collections import defaultdict

"""
Top-Down Island Survival — single-file Pygame
------------------------------------------------
Quick features:
- Procedural island (water/sand/grass) via value noise + radial falloff
- Resources: trees, rocks, berry bushes
- Crafting: Axe (2 wood + 1 stone), Pickaxe (2 wood + 2 stone), Campfire (3 wood + 1 stone)
- Survival stats: health, hunger; hunger ticks down; eating restores hunger
- Day/Night cycle with lighting; campfire emits light at night
- Minimal UI HUD; camera follows player; interact radius for gathering
- Save/Load (F5/F9) — optional convenience

Controls:
  WASD / Arrow keys  Move
  E                  Interact / Gather (near resource)
  1                  Craft Axe
  2                  Craft Pickaxe
  3                  Build Campfire (consumes resources)
  F                  Eat berries (raw) or cooked (if near active campfire)
  M                  Toggle mini-map
  F5 / F9            Save / Load
  ESC                Quit

Requires: pygame (pip install pygame)
"""

# --------------------- Config & Constants ---------------------
WIDTH, HEIGHT = 1024, 640
FPS = 60
TILE_SIZE = 32
MAP_W, MAP_H = 120, 120  # 120x120 tiles ~ 3.8k x 3.8k px world
SEED = random.randint(0, 1_000_000)

# Tile types
WATER, SAND, GRASS = 0, 1, 2

# Resource types
TREE, ROCK, BUSH, CAMPFIRE = "tree", "rock", "bush", "campfire"

# Colors
COLORS = {
    WATER: (40, 90, 160),
    SAND: (224, 204, 150),
    GRASS: (64, 140, 80),
    "tree": (24, 100, 24),
    "rock": (130, 130, 140),
    "bush": (70, 160, 80),
    "player": (230, 90, 50),
    "ui_bg": (0, 0, 0),
    "ui_fg": (240, 240, 240),
    "hp": (200, 50, 50),
    "hunger": (220, 160, 40),
    "shadow": (0, 0, 0),
}

# Gameplay tuning
PLAYER_SPEED = 180  # px/sec
INTERACT_RADIUS = 48
HUNGER_MAX = 100
HEALTH_MAX = 100
HUNGER_TICK_EVERY_SEC = 6.0
HUNGER_DAMAGE_EVERY_SEC = 3.0
CAMPFIRE_LIGHT_RADIUS = 180
CAMPFIRE_DURATION_SEC = 240

# Spawn chances (per grass tile)
TREE_CHANCE = 0.07
ROCK_CHANCE = 0.03
BUSH_CHANCE = 0.05

# --------------------- Utility: Value Noise ---------------------

def _hash_noise(ix, iy, seed):
    # deterministic pseudorandom in [0,1) per integer grid point
    return (math.sin(ix * 127.1 + iy * 311.7 + seed * 0.001) * 43758.5453) % 1.0


def _lerp(a, b, t):
    return a + (b - a) * t


def _smoothstep(t):
    return t * t * (3 - 2 * t)


def value_noise(x, y, scale=24.0, seed=0, octaves=3, persistence=0.5):
    # fractal value noise with bilinear interpolation
    total = 0
    amplitude = 1
    freq = 1.0 / scale
    max_val = 0
    for _ in range(octaves):
        sx, sy = x * freq, y * freq
        x0, y0 = int(math.floor(sx)), int(math.floor(sy))
        dx, dy = sx - x0, sy - y0
        dx, dy = _smoothstep(dx), _smoothstep(dy)
        n00 = _hash_noise(x0, y0, seed)
        n10 = _hash_noise(x0 + 1, y0, seed)
        n01 = _hash_noise(x0, y0 + 1, seed)
        n11 = _hash_noise(x0 + 1, y0 + 1, seed)
        nx0 = _lerp(n00, n10, dx)
        nx1 = _lerp(n01, n11, dx)
        val = _lerp(nx0, nx1, dy)
        total += val * amplitude
        max_val += amplitude
        amplitude *= persistence
        freq *= 2.0
    return total / max_val if max_val > 0 else 0.0


# --------------------- World Generation ---------------------

def generate_world():
    random.seed(SEED)
    tiles = [[WATER for _ in range(MAP_W)] for _ in range(MAP_H)]

    cx, cy = MAP_W / 2, MAP_H / 2
    max_dist = math.hypot(cx, cy)

    # Height map with radial falloff -> island
    for y in range(MAP_H):
        for x in range(MAP_W):
            h = value_noise(x, y, scale=22, seed=SEED, octaves=4, persistence=0.55)
            dist = math.hypot(x - cx, y - cy)
            falloff = 1.0 - (dist / max_dist)
            falloff = max(0.0, min(1.0, falloff ** 1.1))
            height = h * 0.7 + falloff * 0.6
            if height < 0.48:
                tiles[y][x] = WATER
            elif height < 0.54:
                tiles[y][x] = SAND
            else:
                tiles[y][x] = GRASS

    resources = []
    for y in range(MAP_H):
        for x in range(MAP_W):
            if tiles[y][x] == GRASS:
                r = random.random()
                if r < TREE_CHANCE:
                    resources.append({
                        "type": TREE,
                        "x": x * TILE_SIZE + TILE_SIZE // 2,
                        "y": y * TILE_SIZE + TILE_SIZE // 2,
                        "hp": 3,
                    })
                elif r < TREE_CHANCE + ROCK_CHANCE:
                    resources.append({
                        "type": ROCK,
                        "x": x * TILE_SIZE + TILE_SIZE // 2,
                        "y": y * TILE_SIZE + TILE_SIZE // 2,
                        "hp": 3,
                    })
                elif r < TREE_CHANCE + ROCK_CHANCE + BUSH_CHANCE:
                    resources.append({
                        "type": BUSH,
                        "x": x * TILE_SIZE + TILE_SIZE // 2,
                        "y": y * TILE_SIZE + TILE_SIZE // 2,
                        "hp": 1,
                    })
    return tiles, resources


# --------------------- Entities ---------------------

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = 12
        self.health = HEALTH_MAX
        self.hunger = HUNGER_MAX
        self.inventory = defaultdict(int)
        self.has_axe = False
        self.has_pick = False
        self.hunger_timer = 0.0
        self.hunger_damage_timer = 0.0

    @property
    def pos(self):
        return (self.x, self.y)

    def rect(self):
        return pygame.Rect(int(self.x - self.r), int(self.y - self.r), self.r * 2, self.r * 2)

    def move(self, dt, tiles, keys):
        vx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        vy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        if vx == True:
            vx = 1
        if vy == True:
            vy = 1
        speed = PLAYER_SPEED
        if vx and vy:
            speed *= 0.7071
        nx = self.x + vx * speed * dt
        ny = self.y + vy * speed * dt
        # keep inside world and avoid deep water (can't walk on water)
        nx = max(self.r, min(nx, MAP_W * TILE_SIZE - self.r))
        ny = max(self.r, min(ny, MAP_H * TILE_SIZE - self.r))
        if tile_at(tiles, nx, ny) != WATER:
            self.x, self.y = nx, ny

    def update_survival(self, dt, near_campfire=False):
        # Hunger depletes
        self.hunger_timer += dt
        rate = HUNGER_TICK_EVERY_SEC * (0.5 if near_campfire else 1.0)
        if self.hunger_timer >= rate:
            self.hunger_timer -= rate
            self.hunger = max(0, self.hunger - 1)
        # If starving, take damage
        if self.hunger <= 0:
            self.hunger_damage_timer += dt
            if self.hunger_damage_timer >= HUNGER_DAMAGE_EVERY_SEC:
                self.hunger_damage_timer -= HUNGER_DAMAGE_EVERY_SEC
                self.health = max(0, self.health - 2)
        else:
            self.hunger_damage_timer = 0.0

    def eat(self, cooked=False):
        if cooked and self.inventory["cooked"] > 0:
            self.inventory["cooked"] -= 1
            self.hunger = min(HUNGER_MAX, self.hunger + 30)
        elif not cooked and self.inventory["berries"] > 0:
            self.inventory["berries"] -= 1
            self.hunger = min(HUNGER_MAX, self.hunger + 12)


# --------------------- Helpers ---------------------

def tile_at(tiles, px, py):
    tx, ty = int(px // TILE_SIZE), int(py // TILE_SIZE)
    if 0 <= tx < MAP_W and 0 <= ty < MAP_H:
        return tiles[ty][tx]
    return WATER


def world_to_screen(cam, x, y):
    return int(x - cam[0]), int(y - cam[1])


def dist2(ax, ay, bx, by):
    dx, dy = ax - bx, ay - by
    return dx*dx + dy*dy


# --------------------- Save / Load ---------------------
SAVE_PATH = "island_save.json"

def save_game(player, resources, tiles, t_of_day, campfires):
    data = {
        "seed": SEED,
        "player": {
            "x": player.x,
            "y": player.y,
            "health": player.health,
            "hunger": player.hunger,
            "inv": dict(player.inventory),
            "has_axe": player.has_axe,
            "has_pick": player.has_pick,
        },
        "resources": resources,
        "campfires": campfires,
        "time": t_of_day,
    }
    with open(SAVE_PATH, "w") as f:
        json.dump(data, f)


def load_game():
    if not os.path.exists(SAVE_PATH):
        return None
    with open(SAVE_PATH, "r") as f:
        return json.load(f)


# --------------------- Main ---------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Island Survival — Single File")
    clock = pygame.time.Clock()

    tiles, resources = generate_world()

    # Start near island center on grass
    px = MAP_W * TILE_SIZE // 2
    py = MAP_H * TILE_SIZE // 2
    # find nearest grass
    for r in range(0, 400, 12):
        found = False
        for ang in range(0, 360, 15):
            x = px + int(math.cos(math.radians(ang)) * r)
            y = py + int(math.sin(math.radians(ang)) * r)
            if tile_at(tiles, x, y) == GRASS:
                px, py = x, y
                found = True
                break
        if found:
            break

    player = Player(px, py)

    # Time of day [0,1) => 0 dawn, 0.25 day, 0.5 dusk, 0.75 night
    t_of_day = random.random()
    day_length_sec = 480.0  # 8 minutes per full cycle

    # Campfires: list of dict {x,y, t_left}
    campfires = []

    font = pygame.font.SysFont("consolas", 18)
    big_font = pygame.font.SysFont("consolas", 24)

    show_minimap = False
    help_timer = 18.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # --------------- Events ---------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_m:
                    show_minimap = not show_minimap
                elif event.key == pygame.K_F5:
                    save_game(player, resources, tiles, t_of_day, campfires)
                elif event.key == pygame.K_F9:
                    data = load_game()
                    if data:
                        # reload from saved data (seed unchanged for simplicity)
                        p = data["player"]
                        player.x, player.y = p["x"], p["y"]
                        player.health, player.hunger = p["health"], p["hunger"]
                        player.inventory = defaultdict(int, p.get("inv", {}))
                        player.has_axe = p.get("has_axe", False)
                        player.has_pick = p.get("has_pick", False)
                        resources = data.get("resources", resources)
                        campfires = data.get("campfires", [])
                        t_of_day = data.get("time", t_of_day)
                elif event.key == pygame.K_1:
                    # Craft Axe: 2 wood + 1 stone
                    if player.inventory["wood"] >= 2 and player.inventory["stone"] >= 1:
                        player.inventory["wood"] -= 2
                        player.inventory["stone"] -= 1
                        player.has_axe = True
                elif event.key == pygame.K_2:
                    # Craft Pickaxe: 2 wood + 2 stone
                    if player.inventory["wood"] >= 2 and player.inventory["stone"] >= 2:
                        player.inventory["wood"] -= 2
                        player.inventory["stone"] -= 2
                        player.has_pick = True
                elif event.key == pygame.K_3:
                    # Build Campfire: 3 wood + 1 stone
                    if player.inventory["wood"] >= 3 and player.inventory["stone"] >= 1:
                        if tile_at(tiles, player.x, player.y) != WATER:
                            player.inventory["wood"] -= 3
                            player.inventory["stone"] -= 1
                            campfires.append({
                                "x": int(player.x),
                                "y": int(player.y),
                                "t_left": CAMPFIRE_DURATION_SEC,
                            })
                elif event.key == pygame.K_f:
                    # Eat. If near active campfire, cook berries -> cooked
                    near_fire = any(
                        dist2(player.x, player.y, c["x"], c["y"]) <= (CAMPFIRE_LIGHT_RADIUS * 0.6) ** 2 and c["t_left"] > 0
                        for c in campfires
                    )
                    if near_fire and player.inventory["berries"] > 0:
                        # cook one berry -> cooked food
                        player.inventory["berries"] -= 1
                        player.inventory["cooked"] += 1
                    else:
                        # eat (cooked preferred)
                        if player.inventory["cooked"] > 0:
                            player.eat(cooked=True)
                        else:
                            player.eat(cooked=False)

        keys = pygame.key.get_pressed()

        # --------------- Update ---------------
        player.move(dt, tiles, keys)

        # Interact / Gather
        if keys[pygame.K_e]:
            # find closest resource in radius
            best_i, best_d2 = None, INTERACT_RADIUS ** 2
            for i, r in enumerate(resources):
                d2 = dist2(player.x, player.y, r["x"], r["y"])
                if d2 <= best_d2:
                    best_i, best_d2 = i, d2
            if best_i is not None:
                r = resources[best_i]
                if r["type"] == TREE:
                    # faster with axe; otherwise harder
                    dmg = 2 if player.has_axe else 1
                    r["hp"] -= dmg
                    if r["hp"] <= 0:
                        player.inventory["wood"] += random.randint(2, 4)
                        resources.pop(best_i)
                elif r["type"] == ROCK:
                    dmg = 2 if player.has_pick else 1
                    r["hp"] -= dmg
                    if r["hp"] <= 0:
                        player.inventory["stone"] += random.randint(2, 3)
                        resources.pop(best_i)
                elif r["type"] == BUSH:
                    player.inventory["berries"] += random.randint(1, 3)
                    resources.pop(best_i)

        # Update time of day and campfires
        t_of_day = (t_of_day + dt / day_length_sec) % 1.0
        for c in campfires:
            if c["t_left"] > 0:
                c["t_left"] = max(0.0, c["t_left"] - dt)

        # Survival tick
        near_campfire = any(
            dist2(player.x, player.y, c["x"], c["y"]) <= (CAMPFIRE_LIGHT_RADIUS * 0.6) ** 2 and c["t_left"] > 0
            for c in campfires
        )
        player.update_survival(dt, near_campfire=near_campfire)

        help_timer = max(0.0, help_timer - dt)

        # --------------- Camera ---------------
        cam_x = player.x - WIDTH // 2
        cam_y = player.y - HEIGHT // 2
        cam_x = max(0, min(cam_x, MAP_W * TILE_SIZE - WIDTH))
        cam_y = max(0, min(cam_y, MAP_H * TILE_SIZE - HEIGHT))
        camera = (cam_x, cam_y)

        # --------------- Draw World ---------------
        screen.fill((0, 0, 0))

        # draw visible tiles only
        tx0 = int(cam_x // TILE_SIZE)
        ty0 = int(cam_y // TILE_SIZE)
        tx1 = int((cam_x + WIDTH) // TILE_SIZE) + 1
        ty1 = int((cam_y + HEIGHT) // TILE_SIZE) + 1
        tx0 = max(0, tx0)
        ty0 = max(0, ty0)
        tx1 = min(MAP_W, tx1)
        ty1 = min(MAP_H, ty1)

        for ty in range(ty0, ty1):
            for tx in range(tx0, tx1):
                t = tiles[ty][tx]
                color = COLORS[t]
                rx = tx * TILE_SIZE - cam_x
                ry = ty * TILE_SIZE - cam_y
                pygame.draw.rect(screen, color, (rx, ry, TILE_SIZE, TILE_SIZE))

        # resources
        for r in resources:
            sx, sy = world_to_screen(camera, r["x"], r["y"])
            if -40 <= sx <= WIDTH + 40 and -40 <= sy <= HEIGHT + 40:
                if r["type"] == TREE:
                    pygame.draw.circle(screen, COLORS["tree"], (sx, sy), 12)
                    pygame.draw.rect(screen, (110, 70, 30), (sx - 3, sy, 6, 12))
                elif r["type"] == ROCK:
                    pygame.draw.circle(screen, COLORS["rock"], (sx, sy), 10)
                elif r["type"] == BUSH:
                    pygame.draw.circle(screen, COLORS["bush"], (sx, sy), 9)

        # campfires
        for c in campfires:
            sx, sy = world_to_screen(camera, c["x"], c["y"])
            burning = c["t_left"] > 0
            pygame.draw.circle(screen, (150, 80, 20), (sx, sy), 6)
            if burning:
                pygame.draw.circle(screen, (240, 140, 40), (sx, sy), 5)
                # flicker
                if (pygame.time.get_ticks() // 120) % 2 == 0:
                    pygame.draw.circle(screen, (255, 200, 80), (sx, sy - 3), 4)

        # player
        psx, psy = world_to_screen(camera, player.x, player.y)
        pygame.draw.circle(screen, COLORS["player"], (psx, psy), player.r)

        # Lighting overlay (based on time of day)
        # brightness 1.0 at day (t ~ 0.25), 0.35 at night (t ~ 0.75)
        day_phase = math.sin(2 * math.pi * t_of_day)
        # Map [-1,1] -> [night, day]
        brightness = 0.35 + 0.65 * max(0.0, day_phase)
        if brightness < 0.999:
            shade = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            alpha = int(220 * (1.0 - brightness))
            shade.fill((0, 0, 0, alpha))

            # Light from campfires at night
            if alpha > 10:
                for c in campfires:
                    if c["t_left"] <= 0:
                        continue
                    sx, sy = world_to_screen(camera, c["x"], c["y"])
                    # radial gradient
                    radius = CAMPFIRE_LIGHT_RADIUS
                    grad = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    for rr in range(radius, 0, -6):
                        a = int(alpha * (rr / radius) ** 2 * 0.9)
                        pygame.draw.circle(grad, (0, 0, 0, max(0, alpha - a)), (radius, radius), rr)
                    shade.blit(grad, (sx - radius, sy - radius), special_flags=pygame.BLEND_RGBA_SUB)

            screen.blit(shade, (0, 0))

        # --------------- HUD ---------------
        # Panels
        pygame.draw.rect(screen, (0, 0, 0, 120), (12, 12, 280, 98))
        # Health bar
        pygame.draw.rect(screen, (60, 60, 60), (20, 20, 200, 16))
        hpw = int(200 * (player.health / HEALTH_MAX))
        pygame.draw.rect(screen, COLORS["hp"], (20, 20, hpw, 16))
        screen.blit(font.render("HP", True, COLORS["ui_fg"]), (226, 20))
        # Hunger bar
        pygame.draw.rect(screen, (60, 60, 60), (20, 44, 200, 16))
        hgw = int(200 * (player.hunger / HUNGER_MAX))
        pygame.draw.rect(screen, COLORS["hunger"], (20, 44, hgw, 16))
        screen.blit(font.render("Hunger", True, COLORS["ui_fg"]), (226, 44))

        # Inventory
        inv_text = f"Wood:{player.inventory['wood']}  Stone:{player.inventory['stone']}  Berries:{player.inventory['berries']}  Cooked:{player.inventory['cooked']}"
        screen.blit(font.render(inv_text, True, COLORS["ui_fg"]), (20, 72))
        tools_text = f"Axe:{'Y' if player.has_axe else 'N'}  Pick:{'Y' if player.has_pick else 'N'}"
        screen.blit(font.render(tools_text, True, COLORS["ui_fg"]), (20, 92))

        # Tips
        if help_timer > 0:
            tips = [
                "Move: WASD/Arrows | E: Gather | 1:Axe 2:Pick 3:Campfire | F: Eat/Cook | M: Minimap | F5/F9: Save/Load",
            ]
            for i, line in enumerate(tips):
                surf = big_font.render(line, True, (255, 255, 255))
                screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, HEIGHT - 36 - i * 24))

        # Mini-map
        if show_minimap:
            mm_w, mm_h = 200, 200
            mm = pygame.Surface((mm_w, mm_h))
            for yy in range(mm_h):
                for xx in range(mm_w):
                    tx = int(xx / mm_w * MAP_W)
                    ty = int(yy / mm_h * MAP_H)
                    color = COLORS[tiles[ty][tx]]
                    mm.set_at((xx, yy), color)
            # draw player marker
            ptx = int(player.x / (MAP_W * TILE_SIZE) * mm_w)
            pty = int(player.y / (MAP_H * TILE_SIZE) * mm_h)
            pygame.draw.circle(mm, (255, 50, 50), (ptx, pty), 3)
            screen.blit(mm, (WIDTH - mm_w - 12, 12))
            pygame.draw.rect(screen, (255, 255, 255), (WIDTH - mm_w - 12, 12, mm_w, mm_h), 2)

        # --------------- Game Over ---------------
        if player.health <= 0:
            over = big_font.render("You starved. Press ESC to quit.", True, (255, 200, 200))
            screen.blit(over, (WIDTH // 2 - over.get_width() // 2, HEIGHT // 2 - 14))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise
