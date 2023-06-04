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

def imprimir_poblacion(poblacion):
    for i in range(len(poblacion)):
        print(f"Binario: {poblacion[i].binario}, Reales: {poblacion[i].real}, Fitness: {poblacion[i].fitness}")
        # print(type(individuo))

def imprimir_tabla(pob1: list, pob2:list):
	print(f'pob1 len es {len(pob1)}')
	print(f'pob2 len es {len(pob2)}')
	tabla = PrettyTable()
	tabla.field_names = ('Pob inicial','fitness0','','Pob final','fitness1')
	for i in range(len(pob1)):
		tabla.add_row([
			pob1[i].real,
			pob1[i].fitness,
			'',
			pob2[i].real,
			pob2[i].fitness
		])
	print(tabla)
	return