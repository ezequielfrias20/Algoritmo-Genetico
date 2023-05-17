import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand, randint, shuffle
import random


def population_func (variables, size):
    population = []
    #Creamos la poblacion
    if len(variables) == 2:
        population = [[random.uniform(variables[0]['limites'][0], variables[0]['limites'][1]), random.uniform(variables[1]['limites'][0], variables[1]['limites'][1])] for _ in range(size)]
    if len(variables) == 3:
        population = [[random.uniform(variables[0]['limites'][0], variables[0]['limites'][1]), random.uniform(variables[1]['limites'][0], variables[1]['limites'][1]), random.uniform(variables[2]['limites'][0], variables[2]['limites'][1])] for _ in range(size)]
    return population

def fitness_func (population, funcion, F1, F2, max_min):
    fitness = []
    #Creamos la lista con los fitness
    for individual in population:
        value = F1(individual[0], individual[1]) if funcion == '1' else F2(individual[0], individual[1], individual[2])
        fitness.append(value if max_min else 100/(1+value)
)
    return fitness 
# Función de selección de padres utilizando el método de la ruleta
def seleccion_ruleta(poblacion, fitness, num_padres):
    # Calcular la suma total de los valores de fitness
    suma_fitness = sum(fitness)

    # Calcular la probabilidad de selección de cada solución
    probabilidad = [f/suma_fitness for f in fitness]

    # Seleccionar los padres
    padres = []
    for i in range(num_padres):
        # Seleccionar un número aleatorio entre 0 y 1
        r = random.uniform(0, 1)
        # Sumar las probabilidades hasta que se alcance el valor aleatorio
        suma_probabilidad = 0
        for j in range(len(poblacion)):
            suma_probabilidad += probabilidad[j]
            if suma_probabilidad >= r:
                padres.append(poblacion[j])
                break

    return padres

# Función de crossover de un punto
def crossover_un_punto(padre1, padre2):
    # Calcular el punto de crossover
    punto_crossover = 1

    # Generar los hijos a partir de los padres y el punto de crossover
    hijo1 = padre1[:punto_crossover] + padre2[punto_crossover:]
    hijo2 = padre2[:punto_crossover] + padre1[punto_crossover:]

    return hijo1, hijo2

# Función de reproducción utilizando selección por ruleta y crossover de un punto
def reproduccion_ruleta_crossover(poblacion, fitness, tasa_crossover):
    nueva_poblacion = []
    # Seleccionar parejas de padres utilizando el método de la ruleta
    parejas = []
    for i in range(len(poblacion)//2):
        padre1, padre2 = seleccion_ruleta(poblacion, fitness, 2)
        parejas.append([padre1, padre2])

    # Generar nuevos hijos utilizando el crossover de un punto
    hijos = []
    for pareja in parejas:
        if random.uniform(0, 1) < tasa_crossover:
            hijo1, hijo2 = crossover_un_punto(pareja[0], pareja[1])
            hijos.append(hijo1)
            hijos.append(hijo2)
        else:
            hijos.append(pareja[0])
            hijos.append(pareja[1])

    # Combinar padres y hijos en una nueva población
    nueva_poblacion = hijos
    return nueva_poblacion


# Definimos una función para realizar la mutación
def mutate(population, prob_mutacion):
    # Seleccionamos un individuo aleatorio de los mejores individuos
    individuo = random.choice(population)
    # Realizamos una mutación en cada uno de los dos valores del individuo
    for i in range(len(individuo)):
        # Si la probabilidad de mutación es menor que un número aleatorio entre 0 y 1,
        # realizamos la mutación
        if prob_mutacion > random.random():
            # Generamos un nuevo valor aleatorio en el intervalo [-8, 8]
            nuevo_valor = random.uniform(-8, 8)
            # Reemplazamos el valor anterior con el nuevo valor
            individuo[i] = nuevo_valor
    return population.append(individuo)