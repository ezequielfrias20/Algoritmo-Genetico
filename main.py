from AG.AG_simple import *
from AG.AG_elitismo_renormalizacion import *
from AG.AG_sobrante_estocastico import *
from AG.AG_sust_parcial import *
from AG.AG_general import *


############## PARAMETROS #######################
parametros = {
    'AG': '5',
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
    'funcion': '1',
    'max_min': True,
    'renormalizacion': False,
    'tope': 100,
    'paso': 2,
    'elitismo': False,
    'sustitucion': False,
    'p_reemplazo': 0.1,
}

# parametros = solicitud_parametros()

if parametros['AG'] == '1' : AG_simple(parametros)
if parametros['AG'] == '2' : AG_elitismo_renormalizacion(parametros, False, True)
if parametros['AG'] == '3' : AG_elitismo_renormalizacion(parametros, True, False)
if parametros['AG'] == '4' : AG_sust_parcial(parametros)
if parametros['AG'] == '5' : AG_general(parametros)
