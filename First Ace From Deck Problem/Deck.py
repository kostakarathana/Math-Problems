import random as r

class CardDeck:
    def __init__(self) -> None:
        self.total_cards: int = 52
        self.card_types: list[str] = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"] * 4


    def draw(self) -> str:
        card: str = r.choice(self.card_types)

        self.card_types.remove(card)
        return card
    
    # 52 cards
    # 4 aces
    # 48 non-aces
    # possibilities = 1, 2, 3....
    # 1 * 4/52          +            2 * 48/52 * 4/51           +               3 * 48/52 * 47/51 * 4/50                +               4 * 48/52 * 47/51 * 46/59 * 4/49

    

        










        