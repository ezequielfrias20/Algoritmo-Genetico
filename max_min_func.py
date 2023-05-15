import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand, randint, shuffle
import random

############## PARAMETROS #######################
# Rango introducido
x_range = (-8, 8)
y_range = (-8, 8)
# Numero de individuos en una poblacion
population_size = 5
# Poblacion
population = []
# Fitness
fitness = []
# Crossover 
tasa_crossover = 0.8
# mutacion
prob_mutacion = 0.2
# Generaciones
num_generaciones = 1



############## FUNCIONES #######################

# Lo primero que haremos sera definir las funciones
def F1(x,y):
    return x + 2*y - 0.3*np.sin(3*np.pi*x)*0.4*np.cos(4*np.pi*y) + 24

def F2(x,y,z):
    return (x**2+y**2)**0.25*(1+np.sin(50*(x**2+y**2)**0.1)**2) + (x**2+z**2)**0.25*(1+np.sin(50*(x**2+z**2)**0.1)**2) + (z**2+y**2)**0.25*(1+np.sin(50*(z**2+y**2)**0.1)**2)


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
        print(value)

def population_func ():
    population = []
    #Creamos la poblacion
    population = [[random.uniform(x_range[0], x_range[1]), random.uniform(y_range[0], y_range[1])] for _ in range(50)]
    return population

def fitness_func (population):
    fitness = []
    #Creamos la lista con los fitness
    for individual in population:
        value = F1(individual[0], individual[1])
        fitness.append(value)
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
    punto_crossover = random.randint(1, len(padre1)-1)

    # Generar los hijos a partir de los padres y el punto de crossover
    hijo1 = padre1[:punto_crossover] + padre2[punto_crossover:]
    hijo2 = padre2[:punto_crossover] + padre1[punto_crossover:]

    return hijo1, hijo2

# Función de reproducción utilizando selección por ruleta y crossover de un punto
def reproduccion_ruleta_crossover(poblacion, fitness, tasa_crossover):
    # Seleccionar parejas de padres utilizando el método de la ruleta
    parejas = []
    for i in range(len(poblacion)//2):
        padre1, padre2 = seleccion_ruleta(poblacion, fitness, 2)
        parejas.append((padre1, padre2))

    # Generar nuevos hijos utilizando el crossover de un punto
    hijos = []
    for pareja in parejas:
        if random.uniform(0, 1) < tasa_crossover:
            hijo1, hijo2 = crossover_un_punto(pareja[0], pareja[1])
            hijos.append(hijo1)
            hijos.append(hijo2)

    # Combinar padres y hijos en una nueva población
    nueva_poblacion = poblacion + hijos

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

############## PROCESO #######################

# Creamos la poblacion
population = population_func()


# Ejecutar el algoritmo genético durante un número determinado de generaciones
for i in range(num_generaciones):
    
    # Se modifica el fitness para cada individuo
    fitness = fitness_func(population)
    # Realizar la reproducción utilizando selección por ruleta y crossover de un punto
    population = reproduccion_ruleta_crossover(population, fitness, tasa_crossover)
    # Se realiza la mutacion
    mutate(population, prob_mutacion)
 
