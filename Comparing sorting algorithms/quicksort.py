import time

class QuickSort():
    def __init__(self, arr: list[int]):
        self.arr: list[int] = arr
        self.time_taken: float = -1
        
    def sort(self, timerOn:bool = False, printOn:bool = False) -> list[int]:
        if timerOn:
            start = time.time()
            self._qsort_recursive(0, len(self.arr)-1)
            self.time_taken = time.time() - start
        else:
            self._qsort_recursive(0, len(self.arr)-1)
        if printOn:
            print(self.arr)
        return self.arr
    
    def return_time_taken(self) -> float:
        if self.time_taken == -1.0:
            raise ValueError("no calculations yet!")
        else:
            return self.time_taken

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


