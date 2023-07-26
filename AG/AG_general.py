from funciones.common import *
from funciones.graphics import *
from funciones.parameter_request import *
from funciones.funciones_optimizar import F2_T1, F1_T1

def AG_general(parametros): 
    ############## PROCESO #######################

    # Creamos la poblacion
    poblacion = population_func(parametros['variables'], parametros['n_pob'])
    # Obtenemos los valores reales para cada individuo
    for i in range(len(poblacion)):
        poblacion[i].real = binario_a_real(poblacion[i].binario, parametros['variables'])

    # Evaluamos el fitness
    fitness_func(parametros, poblacion, funcion_seleccionada(parametros['funcion']))

    print(parametros)

    pob0 = poblacion
    mejor_ind = poblacion[0]

    mejor_ind_corrida = poblacion[0]
    gen_mejor_ind = 0
    
    gen = 1
    index = 0
    list_fitness = []
    list_ronda = []
    for generacion in range(parametros['n_gen']):

        # mejor_ind_gen = max([ i.fitness for i in poblacion])
        # list_fitness.append(mejor_ind_gen)
        # list_ronda.append(generacion)

        ########################################### RENORMALIZACION ########################################################

        if parametros['renormalizacion'] : poblacion = renormalizacion_lineal(poblacion, parametros['tope'], parametros['paso'])

        #####################################################################################################################

        # Seleccion por Ruleta
        individuos_seleccionados = sobrante_estocastico(poblacion)

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

        ########################################### RENORMALIZACION ########################################################

        # if parametros['renormalizacion'] : poblacion = renormalizacion_lineal(poblacion, parametros['tope'], parametros['paso'])

        #####################################################################################################################

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
     
        # Mejor Individuo de la generacion
        mejor_individuo_algoritmo = copy.deepcopy(poblacion[0])
        for i,ind in enumerate(poblacion):
            if ind.fitness > mejor_individuo_algoritmo.fitness:
                mejor_individuo_algoritmo = copy.deepcopy(ind)
                gen = generacion

        # Mejor Individuo de la corrida
        if (mejor_individuo_algoritmo.fitness > mejor_ind_corrida.fitness):
            mejor_ind_corrida = copy.deepcopy(mejor_individuo_algoritmo)
            gen_mejor_ind = generacion


        list_fitness.append(mejor_individuo_algoritmo.fitness)
        list_ronda.append(generacion)

    ########################################### GRAFICAS ########################################################
    imprimir_tabla(pob0, poblacion)
    print('Mejor Individuo ultima generacion ===>', mejor_individuo_algoritmo.real)
    print('En la generacion ===>', gen)
    print('Mejor Individuo de toda la corrida ===>', mejor_ind_corrida.real)
    print('En la generacion ===>', gen_mejor_ind)
    print('Mejor Individuo fitness ===>', mejor_individuo_algoritmo.fitness)
    print('Mejor Individuo ultima generacion fitness ===>', list_fitness[-1])
    
    imprimir_grafico(list_ronda, list_fitness, poblacion)
    # print(f"Mejor Individuo {mejor_ind.real} en la ronda {ronda}")
    # print(f"Fitness {list_fitness}")