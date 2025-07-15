'''
x people in a room. whats the chance two people share the same birthday?
'''

import random as r

if __name__ == "__main__":

    def generate_birthday() -> int:
        return r.randint(1,365)
    
    iterations = 1000
    people = 23
    recorded_birthday_clashes = 0
    
    for i in range(iterations):
        
        birthday_list: list[int] = []

        for i in range(people):
            birthday_list.append(generate_birthday())
        
        if len(set(birthday_list)) < len(birthday_list):
            recorded_birthday_clashes += 1
    
    print(100*(recorded_birthday_clashes/iterations))