import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand, randint, shuffle
import random
from funciones.common import *
from funciones.graphics import *
from funciones.parameter_request import *
import copy

###################################### TAREA 2 #######################################################

# El objetivo de esta tarea es aplicar a la tarea 1 en la seleccion el metodo de sobrante estocastico.

def AG_sobrante_estocastico(parametros) :
    ############## PROCESO #######################
    # parametros = solicitud_parametros()

    # Creamos la poblacion
    poblacion = population_func(parametros['variables'], parametros['n_pob'])
    pob0 = poblacion
    mejor_ind = poblacion[0]
    index = 0
    ronda = 0
    list_fitness = []
    list_ronda = []
    for generacion in range(parametros['n_gen']):
        
        #Obtenemos los valores reales para cada individuo
        for i in range(len(poblacion)):
            poblacion[i].real = binario_a_real(poblacion[i].binario, parametros['variables'])

        # Evaluamos el fitness
        fitness_func(parametros, poblacion, funcion_seleccionada(parametros['funcion']))

        # Mejor Individuo
        for i,ind in enumerate(poblacion):
            if ind.fitness > mejor_ind.fitness:
                mejor_ind = ind
                index = i
        list_fitness.append(mejor_ind.fitness)
        list_ronda.append(generacion)

        # Seleccion por Sobrante Estocastico
        individuos_seleccionados = sobrante_estocastico(poblacion)

        # Cruce
        poblacion = cruce_ruleta_crossover(individuos_seleccionados, parametros['p_cruce'])

        # Se realiza la mutacion
        mutacion_poblacion(poblacion, parametros['p_muta'])

        #Obtenemos los valores reales para cada individuo
        for ind in range(len(poblacion)):
            poblacion[ind].real = binario_a_real(poblacion[ind].binario, parametros['variables'])

        # Evaluamos el fitness
        fitness_func(parametros, poblacion, funcion_seleccionada(parametros['funcion']))

    ########################################### GRAFICAS ########################################################
    # imprimir_tabla(pob0, poblacion)
    imprimir_grafico(list_ronda, list_fitness, poblacion)
    print(f"Mejor Individuo {mejor_ind.real} en la ronda {ronda}")
    # print(f"Fitness {list_fitness}")
