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

class Data:
    def __init__(self) -> None:
        self.content = []

    def insert(self, val) -> None:
        if len(self.content) == 0:
            self.content.append(val)

        mid = len(self.content) // 2



    def find_median(self):
        pass

