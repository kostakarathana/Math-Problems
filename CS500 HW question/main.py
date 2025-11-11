'''

Consider the problem of maintaining the k-th smallest element in a dynamic set.
For simplicity, you can assume all numbers are distinct. You can use any data structures
discussed in class without implementing them. You do not need to prove the correctness or
analyze the runtime of your algorithms.


(a) Design a deterministic data structure that supports the following operations:
• insert(x): add the number x to the data structure.
• find_median(): returns the median of all numbers in the data structure. If there
are an even number of elements, return the smaller of the two middle values.
Each operation should run in worst-case O(log n) time, where n is the number of elements
in the data structure.


(b) Design a randomized data structure that supports the following operations:
• insert(x): add the number x to the data structure.
• find_kth_element(k): return the k-th smallest number in the data structure. You
can assume there are at least k elements in the data structure.
Each operation should run in expected O(log n) time, where n is the number of elements
in the data structure
'''

import heapq
import random

class Data1:
    def __init__(self) -> None:
        # max-heap via negatives for the lower half
        self.low = []   # stores negatives
        # min-heap for the upper half
        self.high = []  # stores positives

    def insert(self, x) -> None:
        if not self.low:
            heapq.heappush(self.low, -x)
            return

        # Decide which heap gets x
        if x <= -self.low[0]:
            heapq.heappush(self.low, -x)
        else:
            heapq.heappush(self.high, x)

        # Rebalance so len(low) == len(high) or len(low) == len(high)+1
        if len(self.low) < len(self.high):
            # move one from high -> low
            moved = heapq.heappop(self.high)
            heapq.heappush(self.low, -moved)
        elif len(self.low) > len(self.high) + 1:
            # move one from low -> high
            moved = -heapq.heappop(self.low)
            heapq.heappush(self.high, moved)

    def find_median(self):
        if not self.low:
            raise IndexError("No elements")
        # If even count, we return the smaller of the two middles -> top of low
        return -self.low[0]


class _Node:
    __slots__ = ("key", "prio", "left", "right", "size")
    def __init__(self, key):
        self.key = key
        self.prio = random.random()
        self.left = None
        self.right = None
        self.size = 1

def _sz(t):
    return t.size if t else 0

def _pull(t):
    if t:
        t.size = 1 + _sz(t.left) + _sz(t.right)
    return t

def _rotate_right(t):
    # t has left child; bring it up
    x = t.left
    t.left = x.right
    x.right = _pull(t)
    return _pull(x)

def _rotate_left(t):
    # t has right child; bring it up
    x = t.right
    t.right = x.left
    x.left = _pull(t)
    return _pull(x)

def _insert(t, key):
    if not t:
        return _Node(key)
    if key < t.key:
        t.left = _insert(t.left, key)
        if t.left.prio < t.prio:
            t = _rotate_right(t)
    else:
        t.right = _insert(t.right, key)
        if t.right.prio < t.prio:
            t = _rotate_left(t)
    return _pull(t)

def _kth(t, k):
    # 1-indexed: k in [1, _sz(t)]
    if not t or k < 1 or k > _sz(t):
        raise IndexError("k out of range")
    left_size = _sz(t.left)
    if k == left_size + 1:
        return t.key
    elif k <= left_size:
        return _kth(t.left, k)
    else:
        return _kth(t.right, k - left_size - 1)

class Data2:
    def __init__(self) -> None:
        self.root = None

    def insert(self, x) -> None:
        # assumes distinct keys; if duplicates possible, add a count field
        self.root = _insert(self.root, x)

    def find_kth_element(self, k: int):
        return _kth(self.root, k)


