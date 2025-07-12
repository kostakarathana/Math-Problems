import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random as r
import math

def get_random_shift():
    angle = r.uniform(0, 2 * math.pi)
    return [math.cos(angle), math.sin(angle)]

# === Step 1: Generate the random walk ===
num_steps = 1000000
x, y = [0], [0]
for _ in range(num_steps):
    dx, dy = get_random_shift()
    x.append(x[-1] + dx)
    y.append(y[-1] + dy)

# === Step 2: Set up the plot ===
max_dist = max(max(map(abs, x)), max(map(abs, y))) * 1.1
fig, ax = plt.subplots(figsize=(6, 6))
line, = ax.plot([], [], lw=0.5, color='gray', alpha=0.7)
point, = ax.plot([], [], 'ro', markersize=4)

# Bold axes
ax.axhline(0, color='black', linewidth=2)
ax.axvline(0, color='black', linewidth=2)

ax.set_xlim(-max_dist, max_dist)
ax.set_ylim(-max_dist, max_dist)
ax.set_aspect('equal')
ax.grid(True)
plt.tight_layout()

# === Step 3: Animation timing setup ===
fps = 60
total_duration_sec = 10
total_frames = fps * total_duration_sec

# Downsample if needed
step_interval = max(1, len(x) // total_frames)
frame_indices = list(range(0, len(x), step_interval))
if frame_indices[-1] != len(x) - 1:
    frame_indices.append(len(x) - 1)  # ensure the final frame gets plotted

# === Step 4: Animation functions ===
def init():
    line.set_data([], [])
    point.set_data([], [])
    return line, point

def update(frame_num):
    i = frame_indices[frame_num]
    line.set_data(x[:i+1], y[:i+1])
    point.set_data([x[i]], [y[i]])  # FIXED: must pass as lists
    return line, point

ani = animation.FuncAnimation(
    fig, update, frames=len(frame_indices),
    init_func=init, blit=True,
    interval=1000 * total_duration_sec / len(frame_indices)
)

plt.show()