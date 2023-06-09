from funciones.common import *
from funciones.graphics import *
from funciones.parameter_request import *
from funciones.funciones_optimizar import F2_T1, F1_T1

def AG_general(parametros): 
    ############## PROCESO #######################

    print(parametros['variables'])

    # Creamos la poblacion
    poblacion = population_func(parametros['variables'], parametros['n_pob'])
    # Obtenemos los valores reales para cada individuo
    for i in range(len(poblacion)):
        poblacion[i].real = binario_a_real(poblacion[i].binario, parametros['variables'])

    # Evaluamos el fitness
    fitness_func(parametros, poblacion, funcion_seleccionada(parametros['funcion']))

    pob0 = poblacion
    mejor_ind = poblacion[0]
    index = 0
    ronda = 0
    list_fitness = []
    list_ronda = []
    for generacion in range(parametros['n_gen']):

        # mejor_ind_gen = max([ i.fitness for i in poblacion])
        # list_fitness.append(mejor_ind_gen)
        # list_ronda.append(generacion)

        ########################################### RENORMALIZACION ########################################################

        if parametros['renormalizacion'] : poblacion = renormalizacion_lineal(poblacion)

        #####################################################################################################################

        # Seleccion por Ruleta
        individuos_seleccionados = seleccion_ruleta(poblacion)

        # imprimir_poblacion(individuos_seleccionados)

        if parametros['sustitucion'] :
            poblacion = sustitucion_parcial(individuos_seleccionados, parametros)

        else:
            # Cruce
            poblacion = cruce_ruleta_crossover(individuos_seleccionados, parametros['p_cruce'])

            # # Se realiza la mutacion
            mutacion_poblacion(poblacion, parametros['p_muta'])

        # Obtenemos los valores reales para cada individuo
        for ind in range(len(poblacion)):
                poblacion[ind].real = binario_a_real(poblacion[ind].binario, parametros['variables'])

        # Evaluamos el fitness
        fitness_func(parametros, poblacion, funcion_seleccionada(parametros['funcion']))

        ########################################### ELITISMO ########################################################
        if parametros['elitismo']:
            c = len(poblacion)-1
            for i,ind in enumerate(poblacion):
                    if ind.fitness > mejor_ind.fitness:
                        mejor_ind = copy.deepcopy(ind)
                        index = i
                    else :
                        c -=1
            if (c <= 0):
                poblacion[index] = copy.deepcopy(mejor_ind)

        ##############################################################################################################

        mejor_ind_gen = max([ i.fitness for i in poblacion])
        list_fitness.append(mejor_ind_gen)
        list_ronda.append(generacion)

    ########################################### GRAFICAS ########################################################
    # imprimir_tabla(pob0, poblacion)
    print(list_fitness)
    imprimir_grafico(list_ronda, list_fitness, poblacion)
    # print(f"Mejor Individuo {mejor_ind.real} en la ronda {ronda}")
    # print(f"Fitness {list_fitness}")