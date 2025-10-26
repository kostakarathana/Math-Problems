#!/usr/bin/env python3
"""
Zebra-like Turing pattern visualizer (Gray–Scott reaction–diffusion)

Usage:
  python zebra_turing.py

Notes:
- F and k control the pattern type. The defaults below tend to produce stripes.
- Try tweaking F, k to move between spots/stripes/maze-like patterns:
    * More stripey:   F=0.026, k=0.051
    * Spots/rosettes: F=0.035, k=0.065
- Keys:
    r : randomize a fresh initial condition
    s : save current frame to PNG
    q or ESC : quit
"""

import numpy as np
import matplotlib.pyplot as plt
import time

# ------------------------
# Parameters (tweakable)
# ------------------------
N = 256           # grid size (NxN)
Du, Dv = 0.20, 0.1  # diffusion rates (u diffuses faster than v)
F, k = 0.02, 0.04  # feed and kill rates -> tends toward stripes ("zebra")
dt = 15.0             # time step
steps_per_frame = 10 # how many PDE steps between screen updates
seed_noise = 0.02    # random noise amplitude in initial condition

# ------------------------
# Helpers
# ------------------------
def laplacian(z: np.ndarray) -> np.ndarray:
    """Periodic Laplacian via 5-point stencil with wrap-around (torus)."""
    return (
        -4.0 * z
        + np.roll(z, 1, 0) + np.roll(z, -1, 0)
        + np.roll(z, 1, 1) + np.roll(z, -1, 1)
    )

def initialize(N: int, noise: float) -> tuple[np.ndarray, np.ndarray]:
    """Start near the homogeneous fixed point with a noisy perturbation."""
    u = np.ones((N, N), dtype=np.float32)
    v = np.zeros((N, N), dtype=np.float32)

    # Seed a central square with more v (inhibitor) to kick off symmetry breaking
    r = N // 10
    c0 = N // 2
    v[c0 - r:c0 + r, c0 - r:c0 + r] = 1.0

    # Add small random noise across the field
    u += (np.random.rand(N, N).astype(np.float32) - 0.5) * noise
    v += (np.random.rand(N, N).astype(np.float32) - 0.5) * noise
    np.clip(u, 0.0, 1.5, out=u)
    np.clip(v, 0.0, 1.5, out=v)
    return u, v

# ------------------------
# Simulation
# ------------------------
u, v = initialize(N, seed_noise)

fig, ax = plt.subplots(figsize=(6, 6))
im = ax.imshow(v, cmap="gray", origin="lower", vmin=0.0, vmax=1.0, interpolation="bilinear")
ax.set_title("Turing (Gray–Scott) – stripes ~ 'zebra'")
ax.set_xticks([]); ax.set_yticks([])
plt.tight_layout()

running = True
last_save_ts = 0.0

def pde_step(u: np.ndarray, v: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """One explicit Euler step of Gray–Scott model."""
    Lu = laplacian(u)
    Lv = laplacian(v)
    uvv = u * (v * v)

    u += (Du * Lu - uvv + F * (1.0 - u)) * dt
    v += (Dv * Lv + uvv - (F + k) * v) * dt

    # keep values in a reasonable range
    np.clip(u, 0.0, 1.5, out=u)
    np.clip(v, 0.0, 1.5, out=v)
    return u, v

def on_key(event):
    global u, v, running, last_save_ts
    if event.key in ("q", "escape"):
        plt.close(event.canvas.figure)
    elif event.key == "r":
        u, v = initialize(N, seed_noise)
    elif event.key == " ":
        running = not running
    elif event.key == "s":
        # simple debounce to avoid spam if key repeats
        now = time.time()
        if now - last_save_ts > 0.3:
            fname = f"turing_{int(now)}.png"
            plt.imsave(fname, v, cmap="gray", vmin=0.0, vmax=1.0)
            print(f"Saved {fname}")
            last_save_ts = now

fig.canvas.mpl_connect("key_press_event", on_key)

# Main loop
try:
    while plt.fignum_exists(fig.number):
        if running:
            for _ in range(steps_per_frame):
                u, v = pde_step(u, v)
            im.set_data(v)
            # autoscale range a bit for visual contrast (optional; comment out if you prefer fixed)
            im.set_clim(vmin=float(v.min()), vmax=float(v.max()))
        plt.pause(0.001)
except KeyboardInterrupt:
    pass