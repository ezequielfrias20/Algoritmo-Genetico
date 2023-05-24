import numpy as np
from numpy.random import rand, randint, shuffle

def valores_esperados(poblacion: list):
	fit_prom = sum([ind['fitness'] for ind in poblacion])/len(poblacion)
	valores_esperados = [ind['fitness']/fit_prom for ind in poblacion]
	return valores_esperados

def sobrante_estocastico(poblacion: list):
	# Versión sin reemplazo
	val_esp = valores_esperados(poblacion)
	parte_entera = [val//1 for val in val_esp]
	sobrante = [val%1 for val in val_esp]
	nueva_poblacion = []
	for index,val in enumerate(parte_entera):
		k=0
		while k != val:
			nueva_poblacion.append(poblacion[index])
			k+=1
	while len(nueva_poblacion) != len(poblacion):
		for index, val in enumerate(sobrante):
			r = rand()
			if r <= val:
				nueva_poblacion.append(poblacion[index])
			if len(nueva_poblacion) == len(poblacion):
				break
	return nueva_poblacion
