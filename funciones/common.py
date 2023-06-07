import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand, randint, shuffle
import random
from funciones.individuos import Individuo
from funciones.graphics import *
import copy


def bits_por_variable(var):
    m = np.log(max(var['limites'])-min(var['limites'])* (10**var['precision']) + 1)/np.log(2)
    return round(m)


def binario_a_real(lista_binario_individuo, variables):
    indice = 0
    valores_reales_individuo = []

    for var in variables:
        # Valor por cada variable
        valor_binario = lista_binario_individuo[indice: indice + var['bits']]
        substring = sum(
            [bit*2**i for i, bit in enumerate(reversed(valor_binario))])  # Substring
        valor_real = min(var['limites']) + (substring*(max(var['limites']) - min(var['limites'])))/(2**var['bits'] - 1)  # Calculo del valor real
        # Se agrega el valor real con su precision
        valores_reales_individuo.append(round(valor_real, var['precision']))
        indice += var['bits']
    return valores_reales_individuo


def population_func(variables, longitud_poblacion):
    population = []

    # Se suman la longitud de cada individuo para obtener la longitud total del cromosoma.
    bits_totales = sum([var['bits'] for var in variables])
    # Creamos la poblacion, para eso usamos una instancia de un Individuo el cual contiene los datos necesarios para cada uno.
    poblacion = [Individuo({
        'binario': list(np.random.randint(2, size=bits_totales)),
        'fitness': None,
        'p_seleccion': None,
        'v_esperado': None,
    }) for _ in range(longitud_poblacion)]
    return poblacion


def fitness_func(parametros, poblacion, F1, F2):
    for i in range(len(poblacion)):
        value = F1(poblacion[i].real) if parametros['funcion'] == '1' else F2(
            poblacion[i].real)
        poblacion[i].fitness = value if parametros['max_min'] else 100 /(1 + value) # La ec 100 /(1 + value) es para que entre menor valor tenga la evalucion del fitness, el fitness sera mas alto

def valores_esperados(poblacion):
    fit_prom = sum([ind.fitness for ind in poblacion])/len(poblacion)
    valores_esperados = [ind.fitness/fit_prom for ind in poblacion]
    return valores_esperados



def renormalizacion_lineal(poblacion):
  fitness_descendente = sorted(poblacion, key=lambda individuo: individuo.fitness, reverse=True)
  imprimir_poblacion(fitness_descendente)
  min_value = fitness_descendente[-1].fitness
  max_value = fitness_descendente[0].fitness
  for i in range(len(fitness_descendente)):
    fitness_descendente[i].fitness = (len(poblacion) * 2 - (2 * (i))) #Su valor maximo es len(poblacion) * 2 y decrementa en 2
  imprimir_poblacion(fitness_descendente)
  return fitness_descendente

# Función de selección de padres utilizando el método de la ruleta
def seleccion_ruleta(poblacion):
    # Calcular la suma total de los valores de fitness
    suma_fitness = sum([poblacion[i].fitness for i in range(len(poblacion))])

    # Calcular la probabilidad de selección de cada individuo
    for i in range(len(poblacion)):
        poblacion[i].p_seleccion = poblacion[i].fitness / suma_fitness

    list_valores_esperados = valores_esperados(poblacion)
    # Modificamos los valores esperado para cada individuo
    for i in range(len(poblacion)):
        poblacion[i].v_esperado = list_valores_esperados[i]

    # Proceso de Seleccion
    individuos_seleccionados = []
    # Seleccionar un número aleatorio entre 0 y 1
    # Sumar los valores esperados hasta que se alcance el valor aleatorio
    while len(individuos_seleccionados) < len(poblacion):
        suma_ve = 0
        r = random.uniform(0, len(poblacion))
        for j in range(len(poblacion)):
            suma_ve += poblacion[j].v_esperado
            if suma_ve >= r:
                individuos_seleccionados.append(poblacion[j])
                break
    return individuos_seleccionados



# Función de crossover de un punto
def crossover_un_punto(padre1, padre2):
    # Calcular el punto de crossover
    punto_crossover = len(padre1.binario)//2
    valor1 = padre1.binario
    valor2 = padre2.binario

    # Generar los hijos a partir de los padres y el punto de crossover
    hijo1 = Individuo({
        'binario': valor1[:punto_crossover] + valor2[punto_crossover:],
        'fitness': None,
        'p_seleccion': None,
        'v_esperado': None,
    })

    hijo2 = Individuo({
        'binario': valor2[:punto_crossover] + valor1[punto_crossover:],
        'fitness': None,
        'p_seleccion': None,
        'v_esperado': None,
    })
    return hijo1, hijo2



# Función de reproducción utilizando selección por ruleta y crossover de un punto
def cruce_ruleta_crossover(individuos_seleccionados, tasa_crossover):
    # Seleccionar parejas de padres utilizando el método de la ruleta
    parejas = []
    for i in range(0,len(individuos_seleccionados),2):
        padre1 = individuos_seleccionados[i]
        padre2 = individuos_seleccionados[i+1]
        parejas.append([padre1, padre2])

    # Generar nuevos hijos
    hijos = []
    for pareja in parejas:
        if rand() > tasa_crossover:
            hijo1, hijo2 = crossover_un_punto(pareja[0], pareja[1])
            hijos.append(hijo1)
            hijos.append(hijo2)
        else:
            hijos.append(pareja[0])
            hijos.append(pareja[1])

    # Combinar padres y hijos en una nueva población
    return hijos

def mutacion(ind):
	r = rand()
	for i, bit in enumerate(ind.binario):
		r1 = rand()
		if r1>r:
			continue
		ind.binario[i] = 1 if bit==0 else 0
	return ind

# Definimos una función para realizar la mutación
def mutacion_poblacion(pob, p_muta):
    for ind in pob:
        r = rand()
        if r > p_muta:
            continue
        ind = mutacion(ind)

def elitismo(poblacion, mejor_ind, index):
  c = len(poblacion)-1
  for i,ind in enumerate(poblacion):
        if ind.fitness > mejor_ind.fitness:
            mejor_ind = copy.deepcopy(ind)
            index = i
        else :
            c -=1
  if (c <= 0):
        poblacion[index] = copy.deepcopy(mejor_ind)