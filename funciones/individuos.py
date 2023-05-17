
class Individuo():
	def __init__(self,params: dict):
		self.nombre = params['nombre']
		self.valor = params['valor']
		self.fitness = params['fitness']
		self.p_seleccion = params['p_seleccion']
		self.v_esperado = params['v_esperado']
		self.x = params['x']
		self.y = params['y']
		pass
