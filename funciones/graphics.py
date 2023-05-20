import numpy as np
import matplotlib.pyplot as plt
from prettytable import PrettyTable

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

def imprimir_tabla(pob1, fitness1, pob2, fitness2):
	tabla = PrettyTable()
	tabla.field_names = ('Pob inicial','fitness0','','Pob final','fitness1')
	for i in range(len(pob1)):
		tabla.add_row([
			pob1[i],
			fitness1[i],
			'',
			pob2[i],
			fitness2[i]
		])
	print(tabla)
	return