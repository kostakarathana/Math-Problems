'''
Basic mergesort implimentation
'''


def mergesort(X: list) -> list:
    # Base case: a list of 0 or 1 elements is already sorted
    if len(X) <= 1:
        return X

    # Split the list into two halves
    mid = len(X) // 2
    left = mergesort(X[:mid])
    right = mergesort(X[mid:])

    # Merge the sorted halves
    return merge(left, right)


def merge(left: list, right: list) -> list:
    merged = []
    i = j = 0

    # Merge while both lists have elements
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    # Append remaining elements (one of these will be empty)
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged