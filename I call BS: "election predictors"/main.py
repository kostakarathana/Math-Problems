"""
Allan Lichtman often gets credit as the best US election predictor
after he predicted 9 of the last 11 elections. On the surface level it
seems impressive, however is it really?
"""
import random
import sys


class Person:
    def __init__(self):
        self.correct_predictions = 0
        self.incorrect_predictions = 0


def simulate_predictions(elections: int, people: int):
    persons = [Person() for _ in range(people)]

    for i in range(elections):
        for person in persons:
            num = random.randint(1,2)
            if num == 1:
                person.correct_predictions += 1

    return 100*len([person for person in persons if person.correct_predictions >= 9])/people



if __name__ == "__main__":
    elections = 11
    print(simulate_predictions(elections, 10000))









