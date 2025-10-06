'''

- Randomised algorithm
- worst case O(n) runtime
- use quickselect(X, k)

'''

import random as r

def quickselect(arr, k):
    if len(arr) == 1:
        return arr[0]

    pivot = r.choice(arr)

    lows= [x for x in arr if x < pivot]
    highs = [x for x in arr if x > pivot]
    pivots = [x for x in arr if x == pivot]

    if k < len(lows):
        return quickselect(lows, k)
    elif k < len(lows) + len(pivots):
        return pivot
    else:
        return quickselect(highs, k-len(lows) - len(pivots))

def t_largest_elements(X, t):
    n = len(X)
    k = n-t
    threshold = quickselect(X,k)

    result = [x for x in X if x >= threshold]
    return result


