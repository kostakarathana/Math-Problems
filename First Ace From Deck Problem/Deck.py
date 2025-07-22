import random as r

class CardDeck:
    def __init__(self) -> None:
        self.total_cards: int = 52
        self.card_types: list[str] = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.cards: dict[str,int] = {
            "A": 4,
            "2": 4,
            "3": 4,
            "4": 4,
            "5": 4,
            "6": 4,
            "7": 4,
            "8": 4,
            "9": 4,
            "10": 4,
            "K": 4,
            "Q": 4,
            "J": 4,
        }

    def draw(self) -> str:
        card: str = r.choice(self.card_types)

        self.cards[card] -= 1
        if self.cards[card] == 0:
            self.card_types.remove(card)
        return card
    

        










        