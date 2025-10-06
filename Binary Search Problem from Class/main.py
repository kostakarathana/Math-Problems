'''
Consider the problem of deciding whether an element appears in a sorted array.
Given a 0-indexed array S with n elements in ascending order and another element v,
the goal is to return 1 if v appears in S and 0 otherwise. The runtime is measured by
the number of pairwise comparisons between v and elements in S.
Design a deterministic algorithm with worst-case runtime O(log n) and prove that it
achieves this runtime. You can assume that all elements in S are distinct.
'''

def search(arr, v):
    '''
    Takes in a sorted array arr and an integer v. Uses binary search to determine
    if v is in arr in O(log n) time.
    '''

    low = 0
    high = len(arr)-1

    while low <= high:
        mid = (low+high)//2
        if arr[mid] < v:
            low = mid + 1
        elif arr[mid] > v:
            high = mid - 1
        else:
            return 1
    return 0

if __name__ == "__main__":
    # demonstration
    assert(search([1,4,6,7,9],6) == 1)
    assert (search([1, 4, 5, 7, 9], 6) == 0)





