from AG.AG_general import *

############## PARAMETROS #######################1
parametros = {
    'n_pob': 100,
    'n_gen': 500,
    'p_cruce': 0.8,
    'p_muta': 0.002,
    'variables': [{
        'nombre': 'x',
        'limites': [-10, 10],
        'bits': 23, 
        'precision': 6
    },{
        'nombre': 'y',
        'limites': [-10,10],
        'bits': 23,
        'precision': 6
    }],
    'funcion': '3',
    'max_min': True,
    'renormalizacion': True,
    'tope': 100,
    'paso': 1,
    'elitismo': True,
    'sustitucion': True,
    'p_reemplazo': 0.1,
}
# parametros = solicitud_parametros()

AG_general(parametros)