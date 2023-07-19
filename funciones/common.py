import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand, randint, shuffle
import random
from funciones.individuos import Individuo
from funciones.graphics import *
import copy
from funciones.funciones_optimizar import *


def funcion_seleccionada(funcion):
    # Funcion que selecciona la funcion seleccionada
    if funcion == '1':
        return F1_T1
    if funcion == '2':
        return F2_T1
    if funcion == '3':
        return F1_T3
    if funcion == '4':
        return F2_T3
    if funcion == '5':
        return F3_T3


def bits_por_variable(var):
    # Funcion que selecciona los bits por cada variable
    m = np.log((max(var['limites'])-min(var['limites']))
               * (10**var['precision']) + 1)/np.log(2)
    return round(m)


def binario_a_real(lista_binario_individuo, variables):
    # Funcion que transforma de binario a real
    indice = 0
    valores_reales_individuo = []

    #  # Generar la lista de valores aleatorios
    # valor_aleatorio = np.random.uniform(min(var['limites']), max(var['limites']))

    # # # Redondear los valores a la precisión deseada
    # values = round(valor_aleatorio, var['precision'])

    for var in variables:
        # Valor por cada variable
        valor_binario = lista_binario_individuo[indice: indice + var['bits']]
        substring = sum(
            [bit*2**i for i, bit in enumerate(reversed(valor_binario))])  # Substring
        valor_real = min(var['limites']) + (substring*(max(var['limites']) -
                                                       min(var['limites'])))/(2**var['bits'] - 1)  # Calculo del valor real
        # Se agrega el valor real con su precision
        valores_reales_individuo.append(round(valor_real, var['precision']))
        indice += var['bits']
    return valores_reales_individuo


def population_func(variables, longitud_poblacion):
    # Funcion que se encarga de generar una poblacion

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


def fitness_func(parametros, poblacion, F):
    # Funcion que se encarga de evaluar el fitness
    for i in range(len(poblacion)):
        value = F(poblacion[i].real)
        # La ec 100 /(1 + value) es para que entre menor valor tenga la evalucion del fitness, el fitness sera mas alto
        poblacion[i].fitness = value if parametros['max_min'] else 1 / \
            (1+(value))


def valores_esperados(poblacion):
    fit_prom = sum([ind.fitness for ind in poblacion])/len(poblacion)
    valores_esperados = [ind.fitness/fit_prom for ind in poblacion]
    return valores_esperados


def renormalizacion_lineal(poblacion, tope, paso):

    fitness_descendente = sorted(
        poblacion, key=lambda individuo: individuo.fitness, reverse=True)
    for i in range(len(fitness_descendente)):
        # Su valor maximo es len(poblacion) * 2 y decrementa en 2
        fitness_descendente[i].fitness = (tope - (paso * (i)))
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
    random.shuffle(individuos_seleccionados)
    # Seleccionar parejas de padres utilizando el método de la ruleta
    parejas = []
    for i in range(0, len(individuos_seleccionados), 2):
        padre1 = individuos_seleccionados[i]
        padre2 = individuos_seleccionados[i+1]
        parejas.append([padre1, padre2])

    # Generar nuevos hijos
    hijos = []
    for pareja in parejas:
        if rand() < tasa_crossover:
            hijo1, hijo2 = crossover_2_puntos(pareja[0], pareja[1])
            hijos.append(hijo1)
            hijos.append(hijo2)
        else:
            hijos.append(pareja[0])
            hijos.append(pareja[1])

    # Combinar padres y hijos en una nueva población
    return hijos


def crossover_orden(padre1, padre2, len_mascara):
    # generamos un array de bits aleatorios (mascara)
    mascara = list(np.random.randint(2, size=len_mascara))

    # generamos un array para los hijos
    hijo1, hijo2 = [0 for i in range(len_mascara)]

    lista_0 = []  # Aqui guardaremos el valor y posicion del padre1 cuando en la mascara sea 0
    lista_1 = []  # Aqui guardaremos el valor y posicion del padre2 cuando en la mascara sea 1
    for i, bit in enumerate(mascara):
        if (bit == 1):
            # Guardamos el valor del padre1 en el hijo1 en la misma posicion
            hijo1[i] = padre1[i]
            # Almacenamos el valor del padre2 cuando es 1
            lista_1.append({"value": padre2[i], "i": i})
        if (bit == 0):
            # Almacenamos el valor del padre1 cuando es 0
            lista_0.append({"value": padre1[i], "i": i})
            # Guardamos el valor del padre2 en el hijo2 en la misma posicion
            hijo2[i] = padre2[i]
    # Permutamos las listas
    random.shuffle(lista_0)
    random.shuffle(lista_1)

    # Añadimos los valores faltantes a los hijos en sus respectivos indices
    for item in lista_0:
        hijo1[item.i] = item.value
    for item in lista_1:
        hijo2[item.i] = item.value

    return hijo1, hijo2


def metodo_cruce_orden(individuos_seleccionados, tasa_crossover):

    random.shuffle(individuos_seleccionados)
    # Seleccionar parejas de padres utilizando el método de la ruleta
    parejas = []
    for i in range(0, len(individuos_seleccionados), 2):
        padre1 = individuos_seleccionados[i]
        padre2 = individuos_seleccionados[i+1]
        parejas.append([padre1, padre2])

    # Generar nuevos hijos
    hijos = []
    for pareja in parejas:
        if rand() < tasa_crossover:
            padre1 = pareja[0].binario
            padre2 = pareja[1].binario

            hijo1, hijo2 = crossover_orden(padre1, padre2, len(individuos_seleccionados[0].binario))
            # Guardamos hijos
            hijos.append(Individuo({
                'binario': hijo1,
                'fitness': None,
                'p_seleccion': None,
                'v_esperado': None,
            }))
            hijos.append(Individuo({
                'binario': hijo2,
                'fitness': None,
                'p_seleccion': None,
                'v_esperado': None,
            }))
        else:
            hijos.append(pareja[0])
            hijos.append(pareja[1])

    return hijos


def mutacion(ind):
    r = rand()
    for i, bit in enumerate(ind.binario):
        r1 = rand()
        if r1 > r:
            continue
        ind.binario[i] = 1 if bit == 0 else 0
    return ind

# Definimos una función para realizar la mutación


def mutacion_poblacion(pob, p_muta):
    for ind in pob:
        r = rand()
        if r > p_muta:
            continue
        ind = mutacion(ind)

def metodo_mutacion_orden(pob, p_muta):
    for ind in pob:
        r = rand()
        if r > p_muta:
            continue
        ind = mutacion(ind)


def elitismo(poblacion, mejor_ind, index):
    c = len(poblacion)-1
    for i, ind in enumerate(poblacion):
        if ind.fitness > mejor_ind.fitness:
            mejor_ind = copy.deepcopy(ind)
            index = i
        else:
            c -= 1
    if (c <= 0):
        poblacion[index] = copy.deepcopy(mejor_ind)


def sobrante_estocastico(poblacion):
    # Versión sin reemplazo
    val_esp = valores_esperados(poblacion)
    parte_entera = [val//1 for val in val_esp]  # Parte entera de los sobrantes
    sobrante = [val % 1 for val in val_esp]  # Residuo de los sobrantes
    nueva_poblacion = []
    for index, val in enumerate(parte_entera):
        k = 0
        while k != val:
            nueva_poblacion.append(poblacion[index])
            k += 1
    while len(nueva_poblacion) != len(poblacion):
        for index, val in enumerate(sobrante):
            r = rand()
            if r <= val:
                nueva_poblacion.append(poblacion[index])
            if len(nueva_poblacion) == len(poblacion):
                break
    return nueva_poblacion


def comparar_fitness(individuo):
    return individuo.fitness


def crossover_2_puntos(ind1, ind2):
    # Calculamos el primer punto de manera aleatoria
    primer_punto = randint(low=1, high=len(ind1.binario)-1)
    # Calculamos el segundo punto de manera aleatoria
    segundo_punto = randint(low=1, high=len(ind1.binario)-1)
    # Verificamos que el segundo punto sea mayor que el primero
    if primer_punto >= segundo_punto:
        primer_punto, segundo_punto = segundo_punto, primer_punto
    # Realizamos el cruce y creamos los dos hijos
    hijo1 = Individuo({
        'binario': ind1.binario[:primer_punto]+ind2.binario[primer_punto:segundo_punto]+ind1.binario[segundo_punto:],
        'fitness': None,
        'p_seleccion': None,
        'v_esperado': None,
    })
    hijo2 = Individuo({
        'binario': ind2.binario[:primer_punto]+ind1.binario[primer_punto:segundo_punto]+ind2.binario[segundo_punto:],
        'fitness': None,
        'p_seleccion': None,
        'v_esperado': None,
    })
    return hijo1, hijo2


def cruce_sustitucion_parcial(individuos_seleccionados, tasa_crossover, cantidad_individuos_reemplazar):
    # Seleccionar parejas de padres utilizando el método de la ruleta
    parejas = []
    for i in range(0, len(individuos_seleccionados), 2):
        padre1 = individuos_seleccionados[i]
        padre2 = individuos_seleccionados[i+1]
        parejas.append([padre1, padre2])

    # Generar nuevos hijos
    hijos = []

    while len(hijos) < cantidad_individuos_reemplazar:
        for pareja in parejas:
            if rand() < tasa_crossover:
                hijo1, hijo2 = crossover_2_puntos(pareja[0], pareja[1])
                existe_hijo1 = any(getattr(ind, "binario") == getattr(
                    hijo1, "binario") for ind in individuos_seleccionados)
                existe_hijo2 = any(getattr(ind, "binario") == getattr(
                    hijo2, "binario") for ind in individuos_seleccionados)
                if ((len(hijos) < cantidad_individuos_reemplazar) and (not existe_hijo1)):
                    hijos.append(hijo1)
                if ((len(hijos) < cantidad_individuos_reemplazar) and (not existe_hijo2)):
                    hijos.append(hijo2)

    # Combinar padres y hijos en una nueva población
    return hijos


def sustitucion_parcial(poblacion, parametros):
    # Obtenemos la poblacion que se va a proceder a realizar la sustitucion

    # Ordenamos de manera descendente
    individuos_ordenados = sorted(
        poblacion, key=comparar_fitness, reverse=True)
    # Obtenemos la cantidad de individuos que se van a sustituir
    cantidad_individuos_reemplazar = int(
        len(poblacion) * parametros['p_reemplazo'])
    # Aqui se hara el cruce y va a retornar los nuevos individuos que se usaran para el reemplazo
    reemplazo_individuos = cruce_sustitucion_parcial(
        poblacion, 0.1, cantidad_individuos_reemplazar)
    # Se realiza la mutacion de los nuevos individuos
    mutacion_poblacion(reemplazo_individuos, parametros['p_muta'])
    # Se agregan los nuevos individuos a la poblacion
    individuos_ordenados[-cantidad_individuos_reemplazar:] = reemplazo_individuos

    return individuos_ordenados
