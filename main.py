from AG.AG_simple import *
from AG.AG_elitismo_renormalizacion import *
from AG.AG_sobrante_estocastico import *
from AG.AG_sust_parcial import *
from AG.AG_general import *


############## PARAMETROS #######################
parametros = {
    'n_pob': 100,
    'n_gen': 50,
    'p_cruce': 0.8,
    'p_muta': 0.1,
    'variables': [{
        'nombre': 'x',
        'limites': [-10, 10],
        'bits': 37,
        'precision': 10
    },{
        'nombre': 'y',
        'limites': [-10, 10],
        'bits': 37,
        'precision': 10
    }],
    'funcion': '3',
    'max_min': True,
    'renormalizacion': True,
    'tope': 200,
    'paso': 2,
    'elitismo': False,
    'sustitucion': False,
    'p_reemplazo': 0.1,
}

parametros = solicitud_parametros()

AG_general(parametros)
