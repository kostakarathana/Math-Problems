class QuickSort():
    def __init__(self, arr: list[int]):
        self.arr: list[int] = arr
    

    def sort(self):
        self._qsort_recursive(0, len(self.arr)-1)
    
    def _qsort_recursive(self, low: int, high: int) -> None:
        if low < high:
            pi = self._partition(low, high)
            self._qsort_recursive(low, pi - 1)
            self._qsort_recursive(pi + 1, high)

    def _partition(self, low: int, high: int) -> int:
        pivot = self.arr[high]
        i= low - 1
        for j in range(low, high):
            if self.arr[j] < pivot:
                i += 1
                self.arr[i], self.arr[j] = self.arr[j], self.arr[i]
        self.arr[i+1],self.arr[high] = self.arr[high], self.arr[i+1]
        return i + 1

    