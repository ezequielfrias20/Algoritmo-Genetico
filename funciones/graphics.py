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
        print(f"Reales: {poblacion[i].real}, Fitness: {poblacion[i].fitness}")
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

def imprimir_grafico(list_ronda, list_fitness, poblacion):
	fig, axs = plt.subplots(1, 2, figsize=(10, 5))
	# Graficar la lista de valores
	# axs[0].plot([ind.fitness for ind in poblacion])
	axs[0].plot(list_ronda, list_fitness)
	axs[0].set_ylabel('Fitness')
	axs[0].set_xlabel('generacion')
	axs[0].set_title('Evolucion del mejor individuo')

	x = []
	y = []

	for ind in poblacion:
		reales = ind.real
		x.append(reales[0])
		y.append(reales[1])
	axs[1].scatter(x,y)

	# Agregar etiquetas de eje y título
	axs[1].set_xlabel('Eje x')
	axs[1].set_ylabel('Eje y')
	axs[1].set_title('Gráfica de puntos')

	# Mostrar el gráfico
	plt.show()