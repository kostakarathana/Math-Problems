# Quicksort vs Mergesort — Animated Visual Comparison
# Requirements: Python 3.x, matplotlib
# Run: python this_file.py

import random
import itertools
import time
from dataclasses import dataclass
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ----------------------------
# Config
# ----------------------------
N = 32                 # number of items to sort
FPS = 30               # target frames per second
SEED = 42              # set to None for randomized each run
PAUSE_BETWEEN_RUNS = 0 # seconds to wait before animation starts

# Colors
COLOR_DEFAULT = "#9db4ff"
COLOR_ACTIVE  = "#ffb347"
COLOR_PIVOT   = "#ff6961"
COLOR_DONE    = "#77dd77"

# ----------------------------
# Instrumentation helpers
# ----------------------------
@dataclass
class Metrics:
    comparisons: int = 0
    writes: int = 0

# ----------------------------
# Quicksort (in-place, Lomuto partition) — yields states
# ----------------------------
def quicksort_generator(values):
    arr = values[:]  # local working copy
    m = Metrics()
    color = [COLOR_DEFAULT] * len(arr)

    def snapshot(highlight=None, pivot_idx=None, done_range=None):
        """Yield current state: (array copy, color list, metrics snapshot)."""
        cols = color[:]
        if highlight is not None:
            for i in highlight:
                if 0 <= i < len(cols):
                    cols[i] = COLOR_ACTIVE
        if pivot_idx is not None:
            cols[pivot_idx] = COLOR_PIVOT
        if done_range is not None:
            lo, hi = done_range
            for i in range(lo, hi + 1):
                cols[i] = COLOR_DONE
        yield arr[:], cols, Metrics(m.comparisons, m.writes)

    def partition(lo, hi):
        pivot = arr[hi]
        pivot_idx = hi
        i = lo
        # show pivot selection
        yield from snapshot(pivot_idx=pivot_idx)
        for j in range(lo, hi):
            m.comparisons += 1
            # highlight comparison
            yield from snapshot(highlight=[j, pivot_idx], pivot_idx=pivot_idx)
            if arr[j] <= pivot:
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    m.writes += 2
                    yield from snapshot(highlight=[i, j], pivot_idx=pivot_idx)
                i += 1
        if i != hi:
            arr[i], arr[hi] = arr[hi], arr[i]
            m.writes += 2
            yield from snapshot(highlight=[i, hi], pivot_idx=i)
        # segment [lo..i] is placed; mark pivot as done
        yield from snapshot(done_range=(i, i))
        return i

    def _quicksort(lo, hi):
        if lo >= hi:
            if lo == hi:
                # Single element considered done
                yield from snapshot(done_range=(lo, lo))
            return
        # partition
        pgen = partition(lo, hi)
        # run partition generator until it returns pivot index
        pivot_index = None
        while True:
            try:
                state = next(pgen)
                yield state
            except StopIteration as e:
                pivot_index = e.value
                break
        # left
        for state in _quicksort(lo, pivot_index - 1):
            yield state
        # right
        for state in _quicksort(pivot_index + 1, hi):
            yield state

    # drive the generator
    for state in _quicksort(0, len(arr) - 1):
        yield state

    # final sweep: paint all done
    yield arr[:], [COLOR_DONE] * len(arr), Metrics(m.comparisons, m.writes)

# ----------------------------
# Mergesort (top-down) — yields states
# ----------------------------
def mergesort_generator(values):
    arr = values[:]  # local working copy
    m = Metrics()
    color = [COLOR_DEFAULT] * len(arr)

    def snapshot(active=None, done_range=None):
        cols = color[:]
        if active:
            for i in active:
                if 0 <= i < len(cols):
                    cols[i] = COLOR_ACTIVE
        if done_range is not None:
            lo, hi = done_range
            for i in range(lo, hi + 1):
                cols[i] = COLOR_DONE
        yield arr[:], cols, Metrics(m.comparisons, m.writes)

    def merge(lo, mid, hi):
        left = arr[lo:mid+1]
        right = arr[mid+1:hi+1]
        i = j = 0
        k = lo
        # Show the two halves being merged
        yield from snapshot(active=list(range(lo, hi+1)))
        while i < len(left) and j < len(right):
            m.comparisons += 1
            # highlight the source positions conceptually
            yield from snapshot(active=[k])
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            m.writes += 1
            yield from snapshot(active=[k])
            k += 1
        # copy remaining
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            m.writes += 1
            yield from snapshot(active=[k-1])
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            m.writes += 1
            yield from snapshot(active=[k-1])

        # mark merged segment done-ish (stable so far)
        yield from snapshot(done_range=(lo, hi))

    def _mergesort(lo, hi):
        if lo >= hi:
            # single element is trivially done
            yield from snapshot(done_range=(lo, lo))
            return
        mid = (lo + hi)//2
        # sort left
        for s in _mergesort(lo, mid):
            yield s
        # sort right
        for s in _mergesort(mid+1, hi):
            yield s
        # merge
        for s in merge(lo, mid, hi):
            yield s

    # drive
    for state in _mergesort(0, len(arr) - 1):
        yield state

    # final sweep
    yield arr[:], [COLOR_DONE] * len(arr), Metrics(m.comparisons, m.writes)

# ----------------------------
# Utility to pace generators to frames
# ----------------------------
class FramePacer:
    """
    Wrap a generator of states and buffer the latest state so that when
    the generator is exhausted, we keep returning the final state.
    """
    def __init__(self, gen):
        self._gen = gen
        self._final = None
        self._exhausted = False

    def next(self):
        if self._exhausted:
            return self._final
        try:
            state = next(self._gen)
            self._final = state
            return state
        except StopIteration:
            self._exhausted = True
            return self._final

# ----------------------------
# Main: build data, set up animation
# ----------------------------
def main():
    if SEED is not None:
        random.seed(SEED)
    base = list(range(1, N + 1))
    random.shuffle(base)

    # Generators
    qgen = quicksort_generator(base)
    mgen = mergesort_generator(base)

    qpace = FramePacer(qgen)
    mpace = FramePacer(mgen)

    # Matplotlib setup
    plt.rcParams["figure.figsize"] = (12, 6)
    fig = plt.figure(constrained_layout=True)
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 20])

    # Titles row
    ax_title_q = fig.add_subplot(gs[0,0])
    ax_title_m = fig.add_subplot(gs[0,1])
    ax_title_q.axis("off")
    ax_title_m.axis("off")
    title_q = ax_title_q.text(0.5, 0.5, "Quicksort",
                              ha="center", va="center", fontsize=14, weight="bold")
    title_m = ax_title_m.text(0.5, 0.5, "Mergesort",
                              ha="center", va="center", fontsize=14, weight="bold")

    # Bars row
    ax_q = fig.add_subplot(gs[1,0])
    ax_m = fig.add_subplot(gs[1,1])

    # Initialize states
    q_arr, q_col, q_met = qpace.next()
    m_arr, m_col, m_met = mpace.next()

    # Bar containers
    bq = ax_q.bar(range(len(q_arr)), q_arr, color=q_col, align='center')
    bm = ax_m.bar(range(len(m_arr)), m_arr, color=m_col, align='center')

    for ax in (ax_q, ax_m):
        ax.set_xlim(-0.5, len(base)-0.5)
        ax.set_ylim(0, max(base) * 1.1)
        ax.set_xticks([])
        ax.set_yticks([])

    # Textboxes for metrics
    q_text = ax_q.text(0.02, 0.95, "", transform=ax_q.transAxes, va="top", ha="left", fontsize=10)
    m_text = ax_m.text(0.02, 0.95, "", transform=ax_m.transAxes, va="top", ha="left", fontsize=10)

    # FPS pacing
    last_update = time.perf_counter()
    frame_interval = 1.0 / FPS

    def fmt_metrics(name, met: Metrics, arr):
        done = "✓" if all(arr[i] <= arr[i+1] for i in range(len(arr)-1)) else " "
        return (f"{name} {done}\n"
                f"Comparisons: {met.comparisons}\n"
                f"Writes: {met.writes}")

    def update(_frame):
        nonlocal last_update

        # Simple pacing to approximate FPS (not strictly necessary for FuncAnimation, but keeps things even)
        now = time.perf_counter()
        if now - last_update < frame_interval:
            return bq + bm
        last_update = now

        # Advance each algorithm one step (or stay on final)
        q_state = qpace.next()
        m_state = mpace.next()

        q_arr, q_col, q_met = q_state
        m_arr, m_col, m_met = m_state

        # Update bars (heights & colors)
        for rect, h, c in zip(bq, q_arr, q_col):
            rect.set_height(h)
            rect.set_color(c)
        for rect, h, c in zip(bm, m_arr, m_col):
            rect.set_height(h)
            rect.set_color(c)

        # Titles & metrics
        title_q.set_text("Quicksort (Lomuto partition)")
        title_m.set_text("Mergesort (Top-down)")

        q_text.set_text(fmt_metrics("Quicksort", q_met, q_arr))
        m_text.set_text(fmt_metrics("Mergesort", m_met, m_arr))

        return bq + bm

    if PAUSE_BETWEEN_RUNS:
        plt.pause(PAUSE_BETWEEN_RUNS)

    ani = FuncAnimation(fig, update, interval=1000/FPS, blit=False)
    plt.show()

if __name__ == "__main__":
    main()