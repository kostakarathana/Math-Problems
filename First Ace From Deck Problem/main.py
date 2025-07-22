from Deck import CardDeck

if __name__ == "__main__":
    
    iterations = 1000000
    attempts_record: list[int] = []

    for i in range(iterations):
        deck = CardDeck()
        curr: str|None = None
        attempts = 0
        while curr != "A":
            curr = deck.draw()
            attempts += 1
        attempts_record.append(attempts)
    print(sum(attempts_record)/len(attempts_record))



