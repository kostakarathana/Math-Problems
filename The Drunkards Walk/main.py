import matplotlib.pyplot as plt
import random as r
import math

def get_random_shift():
    angle = r.uniform(0, 2 * math.pi)
    return [math.cos(angle), math.sin(angle)]


if __name__ == "__main__":
    # Generate walk
    num_steps = 10000
    x, y = [0], [0]
    for _ in range(num_steps):
        dx, dy = get_random_shift()
        x.append(x[-1] + dx)
        y.append(y[-1] + dy)

    # Set bounds
    max_dist = max(max(map(abs, x)), max(map(abs, y))) * 1.1


    # Plot
    fig, ax = plt.subplots(figsize=(6, 6))
    scatter = ax.scatter(x, y, c=range(len(x)), cmap='viridis', s=10)
    ax.plot(x, y, linewidth=0.5, color='gray', alpha=0.6)
    plt.colorbar(scatter, label='Step Number')

    # ✅ BOLD AXES
    ax.axhline(0, color='black', linewidth=2)  # Bold X-axis
    ax.axvline(0, color='black', linewidth=2)  # Bold Y-axis

    # Setup
    ax.set_xlim(-max_dist, max_dist)
    ax.set_ylim(-max_dist, max_dist)
    ax.set_aspect('equal')
    plt.grid(True)
    plt.tight_layout()
    plt.show()