import random as r

class DiceGame:
    def __init__(self) -> None:
        self.record: list[int] = []

    def roll(self) -> int:
        face: int = r.randint(1,6)
        self.record.append(face)
        return face
    
if __name__ == "__main__":
    dice = DiceGame()
    print(dice.roll())

