'''
Given an m x n 3D list n (like [[1,6,2],[5,2,4],[6,3,2]]) and a number k (like 5)

return True if there's two numbers in the 3D list n that add up to k


'''

from collections import defaultdict

def three_dim_two_sum(n: list[list[int]], k: int) -> bool:
    complements = set()

    for i in range(len(n)):
        curr = n[i]
        for val in curr:
            if val in complements:
                return True
            complements.add(k - val)

    return False


if __name__ == "__main__":
    tests = [
        ([[1, 6, 2], [5, 2, 4], [6, 3, 2]], 100, False),
        ([[1, 2], [5, 2], [3, 2]], 7, True),
        ([[1, 6, 2, 10], [5, 2, 4, 19], [6, 3, 2, 101]], 120, True),
        ([[1, 6, 2, 10, 15], [5, 2, 4, 19,21], [6, 3, 2, 101,21]], 1, False),
        ([[1, 6, 2, 10, 15, 21], [5, 2, 4, 19, 21, 15], [6, 3, 2, 101, 21, 13]], 35, False),
        ([[1], [5], [6]], 11, True)
    ]

    for i, test in enumerate(tests):
        if three_dim_two_sum(test[0], test[1]) != test[2]:
            print(f"fail @ test {i}!")









