import time

class StandardSort():
    '''
    A sorting method that uses pythons standard .sort() method, which
    can sort an array in place.
    '''
    def __init__(self, arr: list[int]):
        self.arr: list[int] = arr
        self.time_taken: float = -1
        
    def sort(self, timerOn:bool = False, printOn:bool = False) -> list[int]:
        if timerOn:
            start = time.time()
            self.arr.sort()
            self.time_taken = time.time() - start
        self.arr.sort()
        if printOn:
            print(self.arr)
        return self.arr
    
    def return_time_taken(self) -> float:
        if self.time_taken == -1.0:
            raise ValueError("no calculations yet!")
        else:
            return self.time_taken


