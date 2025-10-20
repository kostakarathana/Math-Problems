

def quicksort(A):
    if len(A) <= 1:
        return A
    pivot = A[len(A)//2]
    left = [x for x in A if x < pivot]
    equal = [x for x in A if x == pivot]
    right = [x for x in A if x > pivot]

    return quicksort(left) + equal + quicksort(right)

if __name__ == "__main__":
    lst = [1,5,23,6,62,23]
    print(quicksort(lst))