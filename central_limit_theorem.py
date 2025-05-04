import matplotlib.pyplot as plt
from matplotlib.widgets import Slider 
import random as r
import math


def get_mean_from_data():
    data = [i for i in range(0,101)]
    r_selections = [r.choice(data) for _ in range(100)]
    return sum(r_selections)/len(r_selections)
    
def generate_means(num):
    return [get_mean_from_data() for _ in range(num)]

initial_num_means = 100

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)

data_to_graph = generate_means(initial_num_means)
hist = ax.hist(data_to_graph, bins=100)
ax.set_title("Central Limit Theorem in Action")
ax.set_xlabel("Sample Mean")
ax.set_ylabel("Frequency")

ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])  # [left, bottom, width, height] in figure coordinates

mean_slider = Slider(
    ax=ax_slider,              
    label='Number of Means',  
    valmin=10,                # Minimum value of the slider
    valmax=1000,             # Maximum value of the slider
    valinit=initial_num_means, 
    valstep=100                # Slider increments by 100 each step
)

def update(val):
    num_means = int(mean_slider.val)               
    new_data = generate_means(num_means)           
    ax.cla()                                       
    ax.hist(new_data, bins=100)                    
    ax.set_title(f"Central Limit Theorem (Means = {num_means})")  
    ax.set_xlabel("Sample Mean")                   
    ax.set_ylabel("Frequency")                     
    fig.canvas.draw_idle()             

mean_slider.on_changed(update)

# Show the plot window with the interactive slider
plt.show()