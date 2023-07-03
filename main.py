from AG.AG_simple import *
from AG.AG_elitismo_renormalizacion import *
from AG.AG_sobrante_estocastico import *
from AG.AG_sust_parcial import *

############## PARAMETROS #######################
parametros = {
    'AG': '1',
    'n_pob': 50,
    'n_gen': 1,
    'p_cruce': 0.8,
    'p_muta': 0.1,
    'variables': [{
        'nombre': 'x',
        'limites': [-8, 8],
        'bits': 10,
        'precision': 3
    },{
        'nombre': 'y',
        'limites': [-8, 8],
        'bits': 10,
        'precision': 3
    }],
    'funcion': '1',
    'max_min': False
}

parametros = solicitud_parametros()

if parametros['AG'] == '1' : AG_simple(parametros)
if parametros['AG'] == '2' : AG_elitismo_renormalizacion(parametros, False, True)
if parametros['AG'] == '3' : AG_elitismo_renormalizacion(parametros, True, False)
if parametros['AG'] == '4' : AG_sust_parcial(parametros)
