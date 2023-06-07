import copy

def renormalizacion_lineal(poblacion):
  fitness_descendente = sorted(poblacion, key=lambda individuo: individuo.fitness, reverse=True)
  min_value = fitness_descendente[-1]
  max_value = fitness_descendente[len(poblacion)-1]
  for i in range(len(fitness_descendente)):
    fitness_descendente[i].fitness = ((fitness_descendente[i].fitness - min_value) / (max_value - min_value))* (100 - (5 * (i - 1))) + (5 * (i - 1))
  return fitness_descendente

def elitismo(poblacion, mejor_ind):
  c = len(poblacion)-1
  for i,ind in enumerate(poblacion):
        if ind.fitness > mejor_ind.fitness:
            mejor_ind = copy.deepcopy(ind)
            index = i
        else :
            c -=1
  if (c <= 0):
        poblacion[index] = copy.deepcopy(mejor_ind)