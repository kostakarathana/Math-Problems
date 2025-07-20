class BetterPythonCalculator:
    def __init__(self) -> None:
        self.record: list[str] = []

    def add(self, x: float, y: float) -> float:
        self.record.append(f"{x} + {y} = {x+y}")
        return x + y

    def subtract(self,x:float,y:float) -> float:
        self.record.append(f"{x} - {y} = {x-y}")
        return x - y
    
    def multiply(self, x: float, y: float) -> float:
        self.record.append(f"{x} * {y} = {x*y}")
        return x*y
    
    def divide(self, x: float, y: float) -> float:
        self.record.append(f"{x} / {y} = {x/y}")
        return x/y
    
    def see_record(self) -> list[str]:
        return self.record
    


if __name__ == "__main__":
    calc = BetterPythonCalculator()
    calc.add(2,4)
    calc.add(calc.multiply(2,4),calc.multiply(4,6))
    print(calc.see_record())