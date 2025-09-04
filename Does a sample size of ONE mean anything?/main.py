'''
Say I wait for an event to happen that I know has anywhere
from 0% to 100% chance of happening uniformly. What can actually
be said about how likely it was to happen based on one sample?

A real example to visualise:

I am going to flip a biased coin and hope for heads, but I don't know how biased the
coin actually is. It could be 99% biased towards tails (1% heads), or 93% biased towards
heads. Simply, there's an x% chance of getting heads where x is distributed uniformly randomly between 0 -> 100
'''

import random as r

def flip_and_get_data() -> [str, float]:
    r1 = r.random()
    r2 = r.random()
    if r2 < r1:
        return ["Heads", r1]
    else:
        return ["Tails", r1]


if __name__ == "__main__":
    results = []
    total_heads = 0
    total_tails = 0

    r1_heads_total = 0
    r1_tails_total = 0


    for i in range(100000):
        res = flip_and_get_data()
        results.append(res)
        if res[0] == "Heads":
            total_heads += 1
            r1_heads_total += res[1]
        else:
            total_tails += 1
            r1_tails_total += res[1]

    print(r1_heads_total/total_heads)




