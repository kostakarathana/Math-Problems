"""
Simulate a casino to see how to profit
"""
import random

class SlotMachine:
    '''
    Basic slot machine model
    '''
    def __init__(self, edge: int):
        self.edge = edge
        self.profits = 0

    def play(self):
        '''
        With self.edge == 0, this game will return an expected
        profit of $0 over time.
        '''
        self.number = random.randint(1,10000+(self.edge*100))
        if self.number == 1: # major jackpot
            self.profits -= 10000
            return
        if (1 < self.number < 10): # minor jackpot
            self.profits -= 500
            return
        if (10 < self.number < 500): # standard feature win
            self.profits -= 50
            return
        else:
            self.profits += 5 # spin loss



class Casino:
    def __init__(self, slot_machines: list[SlotMachine]):
        self.slot_machines = slot_machines
        self.staff_required = (len(self.slot_machines) // 5) + 1

    def simulate_one_hour(self, people):
        # assume there is one slots machine hit every 5 minutes by each person
        profit = 0
        for i in range(people*12):
            machine = random.choice(self.slot_machines)
            machine.play()

        for slot in self.slot_machines:
            print(slot.profits)
            profit += slot.profits

        return profit # - (self.staff_required*30) # staff, $30 per hour




if __name__ == "__main__":
    machines = [SlotMachine(10),SlotMachine(10), SlotMachine(10), SlotMachine(10), SlotMachine(10)]





