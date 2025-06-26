import time

class NaiveSort():
    def __init__(self, arr: list[int]):
        self.arr: list[int] = arr
        self.time_taken: float = -1

        
    def sort(self, timerOn: bool = False, printOn: bool = False) -> list[int]:
        unsorted: list[int] = self.arr.copy()
        sorted_list: list[int] = []

        start: float = 0.0

        if timerOn:
            start = time.time()

        while unsorted:
            curr_min = min(unsorted)
            sorted_list.append(curr_min)
            unsorted.remove(curr_min)

        if timerOn:
            self.time_taken = time.time() - start

        if printOn:
            print(sorted_list)

        return sorted_list
    
    def return_time_taken(self) -> float:
        if self.time_taken == -1.0:
            raise ValueError("no calculations yet!")
        else:
            return self.time_taken



if __name__ == "__main__":
    ns = NaiveSort([5,2,6,2,6])
    print(ns.sort())
    

