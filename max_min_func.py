import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand, randint, shuffle
import random
from funciones.common import *
from funciones.graphics import *
from funciones.parameter_request import *

############## PARAMETROS #######################
# Rango introducido
variables = [{'nombre': 'x', 'limites': [-8.0, 8.0]}, {'nombre': 'y', 'limites': [-8.0, 8.0]}]
# Numero de individuos en una poblacion
n_pob = 100
# Poblacion
population = []
# Fitness
fitness = []
# Crossover 
p_cruce = 0.8
# mutacion
p_muta = 0.2
# Generaciones
n_gen = 1
# Mejor individuo
mejor_ind = {}



############## FUNCIONES #######################

# Lo primero que haremos sera definir las funciones
def F1(x,y):
    return x + 2*y - 0.3*np.sin(3*np.pi*x)*0.4*np.cos(4*np.pi*y) + 24

def F2(x,y,z):
    return (x**2+y**2)**0.25*(1+np.sin(50*(x**2+y**2)**0.1)**2) + (x**2+z**2)**0.25*(1+np.sin(50*(x**2+z**2)**0.1)**2) + (z**2+y**2)**0.25*(1+np.sin(50*(z**2+y**2)**0.1)**2)


############## PROCESO #######################
parametros = solicitud_parametros()
# Creamos la poblacion
population = population_func(parametros['variables'], parametros['n_pob'])
pop0 = population
mejor_ind = {
    'ind': population[0],
    'ronda': 0,
    'fitness': 0
}
# Se modifica el fitness para cada individuo
fitness = fitness_func(population, parametros['funcion'], F1, F2, parametros['max_min'])
# Ejecutar el algoritmo genético durante un número determinado de generaciones
for i in range(parametros['n_gen']):
    
    # Realizar la reproducción utilizando selección por ruleta y crossover de un punto
    population = reproduccion_ruleta_crossover(population, fitness, parametros['p_cruce'])
    # Se realiza la mutacion
    mutate(population, parametros['p_muta'])
    # Se modifica el fitness para poder ver el mejor individuo
    fitness = fitness_func(population, parametros['funcion'], F1, F2, parametros['max_min'])
    # Seleccionamos el mejor individuo
    for i in range(len(fitness)):
        if fitness[i] > mejor_ind['fitness']:
            mejor_ind = {
                'ind': population[i],
                'ronda': i,
                'fitness': fitness[i]
            }
# print (f"Poblacion final {population}")
print (f"mejor individuo {mejor_ind['ind']}")