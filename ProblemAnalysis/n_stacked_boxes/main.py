'''
We have a stack of boxes, n boxes tall.

Every 'round', we pick a stack of boxes and split it in two halves,
creating two new stacks of boxes. How many boxes are in each stack is up
to us.

When we split a stack, we get points. Namely, we get x*y points, where x is the 
height of the first stack and y is the height of the second stack.

Given n boxes, how should we play optimally to get the best score?
'''
import random as r

class Stack:
    def __init__(self, boxes):
        self.boxes = boxes

# Recursive function to play the game
def play_games(stacks: list) -> int:
    # Base case: no stack left to split
    if all(stack.boxes == 1 for stack in stacks):
        return 0

    # Pick a stack with more than 1 box
    stack = r.choice([s for s in stacks if s.boxes > 1])
    split_point = r.randrange(1, stack.boxes)

    x = split_point
    y = stack.boxes - split_point
    score = x * y

    # Replace the stack with two smaller stacks
    stacks.remove(stack)
    stacks.append(Stack(x))
    stacks.append(Stack(y))

    # Recurse and accumulate score
    return score + play_games(stacks)

if __name__ == "__main__":
    initial_stack = Stack(140)
    stacks = [initial_stack]
    total_score = play_games(stacks)
    print(f"Final score: {total_score}")