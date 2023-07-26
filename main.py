from AG.AG_simple import *
from AG.AG_elitismo_renormalizacion import *
from AG.AG_sobrante_estocastico import *
from AG.AG_sust_parcial import *
from AG.AG_general import *


############## PARAMETROS #######################1
parametros = {
    'n_pob': 100,
    'n_gen': 50,
    'p_cruce': 0.8,
    'p_muta': 0.002,
    'variables': [{
        'nombre': 'x',
        'limites': [-8, 8],
        'bits': 23, 
        'precision': 6
    },{
        'nombre': 'y',
        'limites': [-8,8],
        'bits': 23,
        'precision': 6
    }],
    'funcion': '3',
    'max_min': False,
    'renormalizacion': False,
    'tope': 100,
    'paso': 1,
    'elitismo': False,
    'sustitucion': False,
    'p_reemplazo': 0.1,
}

# parametros = solicitud_parametros()

AG_general(parametros)
