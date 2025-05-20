'''
You are initially given n boxes stacked vertically with the following game rules:

- Split a stack of your choosing every round into two boxes with height x and y, where you decide what x and y are
- Your score for that round is the product of the heights of the two new stacks (score += x*y)
- The scores for each round are added to your total score until you only have n stacks that are 1 box tall

If you play this game optimally, what's the most you could make?
'''

import math

def solution(n: int):
    '''
    Solution: it does not matter how you split the boxes! It just
    counts how many unique pairs are in n boxes
    '''
    return math.factorial(n)/(math.factorial(n-2)*math.factorial(2))
