

def insertion_sort(X: list[int]) -> list[int]:
    '''
    Basic implementation of the insertion sort algorithm.
    '''
    Y = X[:]
    for i in range(1, len(Y)):
        curr = Y[i]
        j = i
        while j > 0 and Y[j-1] > curr:
            Y[j] = Y[j-1]
            j = j-1
        Y[j] = curr
    return Y


if __name__ == "__main__":
    lst = [1,5,3,1,3,6,7,5,1,3,5,62,3,5,6,13,12,12,12,13,11]
    print(insertion_sort(lst))


