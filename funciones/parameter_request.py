import numpy as np
from decimal import Decimal, ROUND_UP
from funciones.common import *

parametros_default = {
    'n_pob': 10,
    'n_gen': 10,
    'p_cruce': 0.8,
    'p_muta': 0.1
}


def solicitud_parametros():
    """Solicitud de parametros de inicio"""
    # AG Seleccionado
    # while True:
    #     try:
    #         AG = str(
    #             input('''Cual opcion desea realizar?
    #             (1) AG simple
    #             (2) AGS1 con renormalización lineal
    #             (3) AGM2 con elitismo
    #             (4) AGM3 con sustitución parcial
    #             (5) AGM4 sin duplicados
    #             ''')).strip().upper()
    #         if AG not in {'1', '2', '3', '4', '5'}:
    #             print('La respuesta debe ser 1, 2, 3, 4 o 5')
    #             continue
    #         break
    #     except:
    #         print('Debe insertar un string válido')
    #         continue
    # Funcion a usar
    while True:
        try:
            funcion = str(
                input('''Cual función desea optimizar?
                    (1) F1 de la Tarea 1
                    (2) F2 de la Tarea 1
                    (3) F1 de la Tarea 3
                    (4) F2 de la Tarea 3
                    (5) F3 de la Tarea 3
                    ''')).strip().upper()
            if funcion not in {'1', '2', '3', '4', '5'}:
                print('La respuesta debe ser 1, 2, 3, 4 o 5')
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
    for i in range(3 if funcion in {'2'} else 2):
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

    
    while True:
        try:
            ag_simple = input(
                'Desea realizar un algoritmo genetico simple? (Y) o (N)  ').strip().upper()
            if ag_simple not in ('Y', 'N'):
                print('La respuesta debe ser Y o N')
                continue
            ag_simple = True if ag_simple == 'Y' else False
            break
        except:
            print('Debe insertar un string válido')
            continue
    if ag_simple:
        elitismo = False
        renormalizacion = False
        sustitucion = False
        tope = 0
        paso = 0
        p_reemplazo = 0.0

    if not ag_simple:
        tope = False
        paso = False
        while True:
            try:
                respuesta = input(
                    'Desea aplicar renormalizacion? (Y) o (N)  ').strip().upper()
                if respuesta not in ('Y', 'N'):
                    print('La respuesta debe ser Y o N')
                    continue
                renormalizacion = True if respuesta == 'Y' else False
                break
            except:
                print('Debe insertar un string válido')
                continue
        if renormalizacion:
            while True:
                try:
                    tope = int(input('Inserte el tope para la renormalizacion:  '))
                    break
                except:
                    print('Debe insertar un número entero')
                    continue
        if renormalizacion:        
            while True:
                try:
                    paso = int(input('Inserte el paso para la renormalizacion:  '))
                    break
                except:
                    print('Debe insertar un número entero')
                    continue

        while True:
            try:
                respuesta = input(
                    'Desea aplicar elitismo? (Y) o (N)').strip().upper()
                if respuesta not in ('Y', 'N'):
                    print('La respuesta debe ser Y o N')
                    continue
                elitismo = True if respuesta == 'Y' else False
                renormalizacion = renormalizacion
                tope = tope if tope else 100
                paso = paso if paso else 1
                break
            except:
                print('Debe insertar un string válido')
                continue

        while True:
            try:
                respuesta = input(
                    'Desea aplicar sustitucion parcial? (Y) o (N)  ' ).strip().upper()
                if respuesta not in ('Y', 'N'):
                    print('La respuesta debe ser Y o N')
                    continue
                sustitucion = True if respuesta == 'Y' else False
                # Esto se hace debido a las codiciones de la tarea que se haga sust parcial con elitismo y renormalizacion
                elitismo = elitismo
                renormalizacion = renormalizacion
                tope = tope if tope else 100
                paso = paso if paso else 1
                break
            except:
                print('Debe insertar un string válido')
                continue
        
        p_reemplazo = 0.0
        if sustitucion :
            # Probabilidad de reemplazo
            while True:
                try:
                    p_reemplazo = float(input('Inserte la Probabilidad de reemplazo:  '))
                    if p_reemplazo > 1.0 or p_reemplazo < 0.0:
                        print('la probabilidad debe ser un número entre 1 y 0')
                        continue
                    break
                except:
                    print('Debe insertar un número de punto flotante')
                    continue
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
            'p_reemplazo': p_reemplazo,
            'renormalizacion': renormalizacion,
            'tope': tope,
            'paso': paso,
            'elitismo': elitismo,
            'sustitucion': sustitucion
            # 'AG': AG
        } | parametros_default
    # Tamaño de Poblacion
    while True:
        try:
            n_pob = int(input('Inserte el tamaño de poblacion:  '))
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
        'p_muta': p_muta,
        'p_reemplazo': p_reemplazo,
        'renormalizacion': renormalizacion,
        'tope': tope,
        'paso': paso,
        'elitismo': elitismo,
        'sustitucion': sustitucion
    }
