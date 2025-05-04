from random import choice as c
import time
def format():
    print("-----------------------------------")

format()
numbers = [1,2,3,4,5,6]
selected = c(numbers)
format()
bet = int(input("what is your bet?  "))
if bet in numbers:
    format()
    print("bet placed successfully, rolling the dice...")
else:
    print("-----------------------------------")
    raise ValueError("that's not a valid bet")




def diceRoller():
    if selected == 1:
        print('''
        
⬜️⬜️⬜️⬜️⬜️
⬜️⬜️⬜️⬜️⬜️
⬜️⬜️⬛️⬜️⬜️
⬜️⬜️⬜️⬜️⬜️
⬜️⬜️⬜️⬜️⬜️
'''
)
    if selected == 2:
        print('''
        
⬜️⬜️⬜️⬜️⬜️
⬜️⬛️⬜️⬜️⬜️
⬜️⬜️⬜️⬜️⬜️
⬜️⬜️⬜️⬛️⬜️
⬜️⬜️⬜️⬜️⬜️
'''
)
    if selected == 3:
        print('''
        
⬜️⬜️⬜️⬜️⬜️
⬜️⬛️⬜️⬜️⬜️
⬜️⬜️⬜️⬛️⬜️
⬜️⬛️⬜️⬜️⬜️
⬜️⬜️⬜️⬜️⬜️
'''
)
    if selected == 4:
        print('''
        
⬜️⬜️⬜️⬜️⬜️
⬜️⬛️⬜️⬛️⬜️
⬜️⬜️⬜️⬜️⬜️
⬜️⬛️⬜️⬛️⬜️
⬜️⬜️⬜️⬜️⬜️
'''
)
    if selected == 5:
        print('''
        
⬜️⬜️⬜️⬜️⬜️
⬜️⬛️⬜️⬛️⬜️
⬜️⬜️⬛️⬜️⬜️
⬜️⬛️⬜️⬛️⬜️
⬜️⬜️⬜️⬜️⬜️
'''
)
    if selected == 6:
        print('''
        
⬜️⬜️⬜️⬜️⬜️
⬜️⬛️⬛️⬛️⬜️
⬜️⬛️⬛️⬛️⬜️
⬜️⬛️⬛️⬛️⬜️
⬜️⬜️⬜️⬜️⬜️
'''
)
time.sleep(2)
diceRoller()
if bet == selected:
    format()
    print(f"you won! You bet {bet} and the number was {selected}")
    format()
else:
    format()
    print(f"you lost! You bet {bet} and the number was {selected}")
    format()