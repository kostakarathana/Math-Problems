import pygame
import random
from collections import deque
import heapq

# Constants
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 40
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Generate random city grid
def generate_city():
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if random.random() < 0.3:  # 30% chance of being a building (obstacle)
                grid[i][j] = 1
    # Choose start and goal on open roads
    start = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    while grid[start[0]][start[1]] == 1:
        start = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    goal = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    while grid[goal[0]][goal[1]] == 1 or goal == start:
        goal = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    return grid, start, goal

# Draw the grid
def draw_grid(screen, grid, closed, frontier_set, path, start, goal):
    screen.fill(WHITE)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            rect = pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if (i, j) == start:
                pygame.draw.rect(screen, GREEN, rect)
            elif (i, j) == goal:
                pygame.draw.rect(screen, RED, rect)
            elif (i, j) in path:
                pygame.draw.rect(screen, YELLOW, rect)
            elif (i, j) in closed:
                pygame.draw.rect(screen, BLUE, rect)
            elif (i, j) in frontier_set:
                pygame.draw.rect(screen, GRAY, rect)
            elif grid[i][j] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # Border

# Get neighbors (up, down, left, right)
def get_neighbors(pos):
    i, j = pos
    neighbors = []
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < GRID_SIZE and 0 <= nj < GRID_SIZE:
            neighbors.append((ni, nj))
    return neighbors

# Heuristic for A* (Manhattan distance)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Search Algorithms Simulation in City")
    clock = pygame.time.Clock()

    grid, start, goal = generate_city()
    algorithm = 'BFS'
    searching = False
    path = []
    frame_delay = 0

    # Variables for search state
    open_queue = None  # For BFS/DFS deque or list, for A* priority queue
    open_set = None
    closed = None
    parent = None
    g_score = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    grid, start, goal = generate_city()
                    searching = False
                    path = []
                    open_queue = None
                    open_set = None
                    closed = None
                    parent = None
                    g_score = None
                if not searching:
                    if event.key == pygame.K_b:
                        algorithm = 'BFS'
                    elif event.key == pygame.K_d:
                        algorithm = 'DFS'
                    elif event.key == pygame.K_a:
                        algorithm = 'A*'
                    elif event.key == pygame.K_s:
                        searching = True
                        closed = set()
                        parent = {start: None}
                        path = []
                        if algorithm == 'BFS':
                            open_queue = deque([start])
                            open_set = set([start])
                        elif algorithm == 'DFS':
                            open_queue = [start]  # Stack
                            open_set = set([start])
                        elif algorithm == 'A*':
                            open_queue = []
                            g_score = {start: 0}
                            f_score = heuristic(start, goal)
                            heapq.heappush(open_queue, (f_score, start))
                            # For A*, no open_set, as multiples allowed

        if searching:
            if frame_delay % 5 == 0:  # Slow down animation
                found = False
                if algorithm in ['BFS', 'DFS']:
                    if open_queue:
                        if algorithm == 'BFS':
                            current = open_queue.popleft()
                        else:
                            current = open_queue.pop()
                        open_set.remove(current)
                        closed.add(current)
                        if current == goal:
                            found = True
                        for neigh in get_neighbors(current):
                            if grid[neigh[0]][neigh[1]] == 1:
                                continue
                            if neigh not in closed and neigh not in open_set:
                                open_queue.append(neigh)
                                open_set.add(neigh)
                                parent[neigh] = current
                elif algorithm == 'A*':
                    if open_queue:
                        f, current = heapq.heappop(open_queue)
                        if current in closed:
                            pass
                        elif f > g_score.get(current, float('inf')) + heuristic(current, goal):
                            pass
                        else:
                            closed.add(current)
                            if current == goal:
                                found = True
                            for neigh in get_neighbors(current):
                                if grid[neigh[0]][neigh[1]] == 1:
                                    continue
                                tentative_g = g_score[current] + 1
                                if tentative_g < g_score.get(neigh, float('inf')):
                                    parent[neigh] = current
                                    g_score[neigh] = tentative_g
                                    new_f = tentative_g + heuristic(neigh, goal)
                                    heapq.heappush(open_queue, (new_f, neigh))
                if found:
                    searching = False
                if not open_queue:
                    searching = False
            frame_delay += 1

        # Reconstruct path if search done and goal reached
        if not searching and parent is not None and goal in parent:
            current = goal
            path = []
            while current is not None:
                path.append(current)
                current = parent.get(current)
            path.reverse()
            if path[0] != start:
                path = []

        # Prepare frontier_set for drawing
        if searching:
            if algorithm in ['BFS', 'DFS']:
                frontier_set = open_set
            else:
                frontier_set = set([pos for _, pos in open_queue])
        else:
            frontier_set = set()

        # Draw
        draw_grid(screen, grid, closed or set(), frontier_set, path, start, goal)

        # Display text
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Algorithm: {algorithm} (B:BFS, D:DFS, A:A*)", True, BLACK)
        screen.blit(text, (10, 10))
        text = font.render("Press S to start, R to regenerate city", True, BLACK)
        screen.blit(text, (10, 40))
        if searching:
            text = font.render("Searching...", True, BLACK)
        elif path:
            text = font.render("Path found!", True, GREEN)
        else:
            text = font.render("No path found", True, RED)
        screen.blit(text, (10, 70))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()