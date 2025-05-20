'''
One of my mates is in charge of a very large residential building with only 5 elevators that
reach 50 different floors. His residents have been complaining that the waitimes for the elevators 
are ridiculous during long hours. He can't fix the hardware and has no room for more elevators, but
he can make the software better. Here are the current restrictions:

- The elevators, once a floor is pressed, will move one floor per second until they reach the desired floor. 
- People can either call from the ground floor up to a certain level or from a numbered level down to ground. 
- Once an elevator hits the desired floor, it stays open for five seconds, then continues to it's next call.
- The elevators cannot hold more than 5 people each

- For safety and simplicity, he gave his residents keycards that they simply tap on a screen as they enter the elevator room
- Once the resident taps their card, the elevator system instantly lets them know on the screen which elevator will take them up. 
Right now, the number the system choses is random, so not effecient at all!

He wants me to draft up a python algorithm that simulates this scenario and minimises waittime for everybody.
'''

