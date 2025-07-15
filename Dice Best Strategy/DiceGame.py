import random as r

class DiceGame:
    def __init__(self) -> None:
        self.face_record: list[int] = []
        self.cash_record: list[int] = []
        self.cash: int = 0

    def roll_and_result(self) -> bool:
        face: int = r.randint(1,6)
        self.face_record.append(face)
        
        if face != 6:
            self.cash += face
            self.cash_record.append(self.cash)
            return True # means game is still on
        else:
            self.cash = 0
            self.cash_record.append(self.cash)
            return False
    
    def get_face_record(self) -> list[int]:
        return self.face_record

    def get_cash_record(self) -> list[int]:
        return self.cash_record



        
    
if __name__ == "__main__":
    dice: DiceGame = DiceGame()
    
    

