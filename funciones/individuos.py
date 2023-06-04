
class Individuo():
	def __init__(self,params):
		self.binario = params['binario']
		self.fitness = params['fitness']
		self.p_seleccion = params['p_seleccion']
		self.v_esperado = params['v_esperado']
		self.real = None
		pass
	
	def __str__(self):
    	 return f"Valor Binario: {self.binario}"
	
