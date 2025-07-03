'''
A casino-addicted friend says that he's been to the casino "over 200 times" in his life and that he is still profitable long
term. See how true that is with statistics. Assumptions:

- Bet 5 times in one night (low end)
- All bets were on red/black roulette wheel (some of the best odds in the casino)
- He bet $20 on each spin (so $100 per trip spent), exact amount of money doesn't matter though

What are the chances he's telling the truth?

RESULTS: 

After simulating his situation one million times, the chance
of being profitable after 200 trips to the casino with 5 bets per trip
on a roulette wheel is ~4.5%. So, its not unreasonable that he might
be telling the truth. 

He shouldn't push his luck though. If he goes another 800 times over his lifetime, his chance of profitability 
would be ~0.05%


'''

import random as r

if __name__ == "__main__":
    simulations: int = 10000
    profits_record : int = 0
    total_trips: int = 800
    bets_per_trip: int = 5

    for i in range(simulations):
        profits = 0
        for _ in range(total_trips):
            for i in range(bets_per_trip):
                if r.randint(1,1000) <= 474: # simulates american roulette odds
                    profits += 20
                else:
                    profits -= 20
        if profits > 0:
            profits_record += 1
    
    print(100*profits_record/simulations)





