import numpy as np
from decimal import Decimal, ROUND_UP
from funciones.common import *

parametros_default = {
    'n_pob': 3,
    'n_gen': 20,
    'p_cruce': 0.8,
    'p_muta': 0.1
}


def solicitud_parametros():
    """Solicitud de parametros de inicio"""
    # Funcion a usar
    while True:
        try:
            funcion = str(
                input('Cual función desea optimizar? (1)F1 o (2)F2?  ')).strip().upper()
            if funcion not in {'1', '2'}:
                print('La respuesta debe ser 1 o 2')
                continue
            break
        except:
            print('Debe insertar un string válido')
            continue
    # Máximo o minimo
    while True:
        try:
            max_min = str(
                input(f'Desea (1)maximizar o (2)minimizar la función F{funcion}:  '))
            if max_min not in {'1', '2'}:
                print('La respuesta debe ser 1 o 2')
                continue
            break
        except:
            print('Debe insertar un string válido')
            continue
    # Variables
    nombre_variable = ('x', 'y', 'z')
    variables = []
    for i in range(int(funcion)+1):
        while True:
            try:
                limite_inferior = float(
                    input('Inserte el limite inferior de {}:  '.format(nombre_variable[i])))
                break
            except:
                print('El límite inferior debe ser un número de punto flotante.')
                continue
        while True:
            try:
                limite_superior = float(
                    input('Inserte el limite superior de {}:  '.format(nombre_variable[i])))
                break
            except:
                print('El límite superior debe ser un número de punto flotante.')
                continue
        variables.append({
            'nombre': nombre_variable[i],
            'limites': [limite_inferior, limite_superior],
            'bits': None,
            'precision': None
        })
    # Precision
    while True:
        try:
            num_precision = int(input('Inserte la precision: '))
            break
        except:
            print('El número de la precision debe ser un número entero')
            continue
    # Calculo de precision
    for var in variables:
        var.update({
            'precision': num_precision
        })

    # Calculo del numero de bits por variable
    for var in variables:
        var.update({
            'bits': bits_por_variable(var)
        })
    # Continuar con parámetros standar
    while True:
        try:
            respuesta = input(
                'Desea modificar los parámetros estandar del algoritmo genético? (Y) o (N)  ').strip().upper()
            if respuesta not in ('Y', 'N'):
                print('La respuesta debe ser Y o N')
                continue
            continuar = True if respuesta == 'Y' else False
            break
        except:
            print('Debe insertar un string válido')
            continue
    if not continuar:
        return {
            'variables': variables,
            'funcion': funcion,
            'max_min': True if max_min == '1' else False,
        } | parametros_default
    # Tamaño de Poblacion
    while True:
        try:
            n_pob = int(input('Insete el tamaño de poblacion:  '))
            if n_pob % 2 == 1:
                print('Por facilidada de cálculo debe insertar un mútiplo de 2')
                continue
            break
        except:
            print('Debe insertar un número entero')
            continue
    # Cantidad de generaciones
    while True:
        try:
            n_gen = int(input('Inserte la cantidad de generaciones:  '))
            break
        except:
            print('Debe insertar un número entero')
            continue
    # Probabilidad de Cruce
    while True:
        try:
            p_cruce = float(input('Inserte la Probabilidad de Cruce:  '))
            if p_cruce > 1.0 or p_cruce < 0.0:
                print('la probabilidad debe ser un número entre 1 y 0')
                continue
            break
        except:
            print('Debe insertar un número de punto flotante')
            continue
    # Probabilidade de mutacion
    while True:
        try:
            p_muta = float(input('Inserte la Probabilidad de Mutacion:  '))
            if p_muta > 1.0 or p_muta < 0.0:
                print('la probabilidad debe ser un número entre 1 y 0')
                continue
            break
        except:
            print('Debe insertar un número de punto flotante')
            continue
    return {
        'variables': variables,
        'funcion': funcion,
        'max_min': True if max_min == '1' else False,
        'n_pob': n_pob,
        'n_gen': n_gen,
        'p_cruce': p_cruce,
        'p_muta': p_muta
    }
