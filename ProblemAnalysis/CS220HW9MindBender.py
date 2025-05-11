'''
Let S = {1, 2, 3, . . . , 9} be the numbers 1 through 9 and let π be a uniformly random
permutation of S where πi is the ith element of π. For instance, we could have
π = (1, 2, 5, 6, 3, 8, 9, 4, 7) in which case π3 = 5. In a slight abuse of notation, we also
define π10 as π1.
Next, define the random variable X(π) = P9
i=1 |πi+1 − πi|. For instance, if we have
that π = (1, 2, 5, 6, 3, 8, 9, 4, 7) then we would have that
X(π) = |2 − 1| + |5 − 2| + |6 − 5| + |3 − 6| + |8 − 3| + |9 − 8| + |4 − 9| + |7 − 4| + |1 − 7|
= 1 + 3 + 1 + 3 + 5 + 1 + 5 + 3 + 6
= 28.
What is the probability that X achieves its minimum possible value? In partic-
ular if π0 is the permutation which minimizes X, then what is P(X = X(π0))?

'''
import random as r
import copy

def getXpi(S: list):
    sum = 0
    for i in range(0,8):
        sum += abs(S[i+1] - S[i])
    sum += abs(S[8] - S[0])
    return sum


combos = {}
standard_list = [1,2,3,4,5,6,7,8,9]
count = 0
for i in range(1000000):
    combo = copy.deepcopy(standard_list)
    r.shuffle(combo)
    val = getXpi(combo)
    if val == 16: # lowest possible value
        count += 1


print(count)
 



    



