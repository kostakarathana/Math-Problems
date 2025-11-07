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

class Data:
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
