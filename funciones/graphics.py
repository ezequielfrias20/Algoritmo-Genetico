import numpy as np
import matplotlib.pyplot as plt

def show(population):
    x_axis=np.arange(-8,8,0.02)
    y_axis=np.arange(-8,8,0.02)
    for individuo in population:
        x = individuo[0]
        y = individuo[1]
        plt.plot(x,y,'x')
    plt.plot(x_axis,y_axis)
    plt.show()

def printer(list, title):
    print(title)
    for value in list:
        print(f"x: {value[0]}, y: {value[1]}")