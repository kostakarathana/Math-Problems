# The Elevator Problem

## Elevator Constraints

- **Number of floors:** 150
- **Expected hourly passengers (6am- 8am):** 200 (mainly ground-to-floor)
- **Expected hourly passengers (7am- 9am):** 1000 (mainly ground-to-floor)
- **Expected hourly passengers (9am- 5pm):** 200 (mainly inter-floor)
- **Expected hourly passengers (5pm- 10pm):** 600 (mainly inter-floor)
- **Expected hourly passengers (10pm - 6am):** 30 

- **Elevator speed:** 1 floor per second
- **Trade-off:** Each elevator added reduces available leasing space
- **Trade-off:** When stopped, an elevator remains stationary on the floor for 20 seconds
- **Building type:** Office (hence why ground-to-high-floor travel is most common during morning, floor-to-floor travel is more common during the day, and floor-to-ground is more common in the afternoon)


## The Problem's Background

The client, Mr. Green, wants to build this elevator system, but he has some issues. He predicts in construction cost, maintenence, and lease potential losses that each extra elevator will have a 10 year cost of ~15 million dollars. So, he asks for an elevator system that, based on the aforementioned constraints, minimises the number of elevators needed. 

As for the passenger experience, he defines 5 categories of experiences: 

- **Waittime experience:** There are 5 categories for waittime: Excellent, Good, Average, Poor, and Abysmal. They are defined by:
    - If an elevator takes less than 1 minute to pick up the passenger, it's an excellent waittime
    - If an elevator takes between 1 minute and 3 minutes to pick up the passenger, it's a good waittime
    - If an elevator takes between 3 minutes and 5 minutes to pick up the passenger, it's an average waittime
    - If an elevator takes between 5 minutes and 10 minutes to pick up the passenger, it's a poor waittime
    - If an elevator takes more than 10 minutes to pick up the passenger, it's an abysmal waittime
    

- **Traversal experience:** There are 5 categories for traversal: Excellent, Good, Average, Poor, and Abysmal. For an individual passenger, they are defined by:
    - If an elevator stops less than or equal to once per 10 floors travelled, it is an excellent traversal experience
    - If an elevator stops between 2 and 3 times per 10 floors travelled, it is a good traversal experience
    - If an elevator stops between 3 and 4 times per 10 floors travelled, it is an average traversal experience
    - If an elevator stops between 4 and 6 times per 10 floors travelled, it is a poor traversal experience
    - If an elevator stops more than 6 times per 10 floors travelled, it is an abysmal traversal experience
   
## The Problem

The client wants to reduce cost by building the least amount of elevators, but he doesn't want a bad elevator system that annoys everyone either, because once it is built, there's no changing it. He defines that throughout any given hour of the day, the passengers' experience must be distrubuted as:


- **Waittime experience:** 
    - Abysmal: 0% 
    - Poor: < 5%
    - Average: < 20%
    - Good: >50%
    - Excellent: flexible, but ideally high % during off-peak times.
    

- **Traversal experience:** There are 5 categories for traversal: Excellent, Good, Average, Poor, and Abysmal. For an individual passenger, they are defined by:
    - If an elevator stops less than or equal to once per 10 floors travelled, it is an excellent traversal experience
    - If an elevator stops between 2 and 3 times per 10 floors travelled, it is a good traversal experience
    - If an elevator stops between 3 and 4 times per 10 floors travelled, it is an average traversal experience
    - If an elevator stops between 4 and 6 times per 10 floors travelled, it is a poor traversal experience
    - If an elevator stops more than 6 times per 10 floors travelled, it is an abysmal traversal experience
