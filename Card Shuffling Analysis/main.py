'''
Assuming that 100 000 decks are shuffled every minute, how long
would it take, on average, for two shuffled decks to be the same? 
'''

import math

if __name__ == "__main__":

    deck_sizes = [i for i in range(1,52)]
    time_to_get_pair: list[float] = []

    for size in deck_sizes:
        time_to_get_pair.append(math.factorial(size)/100_000)
    
    for i, time in enumerate(time_to_get_pair):
        if time < 1e-6:
            cleaned_time = time * 1e9
            unit = "nanoseconds"
        elif time < 1e-3:
            cleaned_time = time * 1e6
            unit = "microseconds"
        elif time < 1:
            cleaned_time = time * 1e3
            unit = "milliseconds"
        elif time < 60:
            cleaned_time = time
            unit = "seconds"
        elif time < 3600:
            cleaned_time = time / 60
            unit = "minutes"
        elif time < 86400:
            cleaned_time = time / 3600
            unit = "hours"
        elif time < 31_536_000:
            cleaned_time = time / 86400
            unit = "days"
        elif time < 315_360_000:
            cleaned_time = time / 31_536_000
            unit = "years"
        elif time < 31_536_000_000:
            cleaned_time = time / 315_360_000
            unit = "decades"
        else:
            cleaned_time = time / 31_536_000_000
            unit = "centuries"

        print(f'''
    {deck_sizes[i]} cards: {cleaned_time:.3g} {unit}
              ''')
    


