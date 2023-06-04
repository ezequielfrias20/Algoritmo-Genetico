import numpy as np
import matplotlib.pyplot as plt
from numpy.random import rand, randint, shuffle
import random
from funciones.common import *
from funciones.graphics import *
from funciones.parameter_request import *

############## PARAMETROS #######################
parametros = {
    'n_pob': 50,
    'n_gen': 20,
    'p_cruce': 0.8,
    'p_muta': 0.1,
    'variables': [{
        'nombre': 'x',
        'limites': [-8, 8],
        'bits': 10,
        'precision': 2
    },{
        'nombre': 'y',
        'limites': [-8, 8],
        'bits': 10,
        'precision': 2
    }],
    'funcion': '1',
    'max_min': False
}


############## FUNCIONES #######################

# Lo primero que haremos sera definir las funciones
def F1(x):
    return x[0] + 2*x[1] - 0.3*np.sin(3*np.pi*x[0])*0.4*np.cos(4*np.pi*x[1]) + 24


def F2(x):
    return (x[0]**2+x[1]**2)**0.25*(1+np.sin(50*(x[0]**2+x[1]**2)**0.1)**2) + (x[0]**2+x[2]**2)**0.25*(1+np.sin(50*(x[0]**2+x[2]**2)**0.1)**2) + (x[2]**2+x[1]**2)**0.25*(1+np.sin(50*(x[2]**2+x[1]**2)**0.1)**2)


############## PROCESO #######################
# parametros = solicitud_parametros()

# Creamos la poblacion
poblacion = population_func(parametros['variables'], parametros['n_pob'])
pob0 = poblacion
mejor_ind = poblacion[0]
ronda = 0
list_fitness = []
list_ronda = []
for generacion in range(parametros['n_gen']):
    #Obtenemos los valores reales para cada individuo
    for i in range(len(poblacion)):
        poblacion[i].real = binario_a_real(poblacion[i].binario, parametros['variables'])

    # Evaluamos el fitness
    fitness_func(parametros, poblacion, F1, F2)
    # Seleccion
    individuos_seleccionados = seleccion_ruleta(poblacion)

    # Cruce
    poblacion = cruce_ruleta_crossover(individuos_seleccionados, parametros['p_cruce'])

    # Se realiza la mutacion
    mutacion_poblacion(poblacion, parametros['p_muta'])

    #Obtenemos los valores reales para cada individuo
    for ind in range(len(poblacion)):
        poblacion[ind].real = binario_a_real(poblacion[ind].binario, parametros['variables'])

    # Evaluamos el fitness
    fitness_func(parametros, poblacion, F1, F2)

    for ind in poblacion:
        if ind.fitness > mejor_ind.fitness:
            mejor_ind = ind
            ronda = generacion
    
    list_fitness.append(mejor_ind.fitness)
    list_ronda.append(generacion)


imprimir_tabla(pob0, poblacion)
print(f"Mejor Individuo {mejor_ind.real} en la ronda {ronda}")
print(f"Mejor Individuo {mejor_ind.real} en la ronda {ronda}")

fig, axs = plt.subplots(1, 2, figsize=(10, 5))
# Graficar la lista de valores
# axs[0].plot([ind.fitness for ind in poblacion])
axs[0].plot(list_ronda, list_fitness)
axs[0].set_ylabel('Fitness')
axs[0].set_xlabel('generacion')
axs[0].set_title('Evolucion del mejor individuo')

x = []
y = []

for ind in poblacion:
    reales = ind.real
    x.append(reales[0])
    y.append(reales[1])
axs[1].scatter(x,y)

# Agregar etiquetas de eje y título
axs[1].set_xlabel('Eje x')
axs[1].set_ylabel('Eje y')
axs[1].set_title('Gráfica de puntos')

# Mostrar el gráfico
plt.show()
