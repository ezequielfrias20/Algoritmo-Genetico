import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand, randint, shuffle
import random

import copy

def crossover_orden(padre1, padre2, len_mascara):
    # generamos un array de bits aleatorios (mascara)
    mascara = list(np.random.randint(2, size=len_mascara))

    # generamos un array para los hijos
    hijo2 =  [0 for i in range(len_mascara)]
    hijo1 = [0 for i in range(len_mascara)]

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
