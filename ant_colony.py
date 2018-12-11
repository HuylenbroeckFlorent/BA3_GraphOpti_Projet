from read_QAP import read_QAP

size=0
D=[]
F=[]

def _init(path):
	size,D,F=read_QAP(path)

def ant(alpha, beta):
	return

def compute_probability(alpha,beta,s,elements):
	return

def visible(e1,e2):
	return

def ant_colony(N,alpha,beta,Q,omega):
	return

def drop_pheromones(s,Q):
	return

def evaporate_pheromone(omega):
	return

def _print():
	print(size)
	print('\nD=')
	for d in D:
		print(d)
	print('\nF=')
	for f in F:
		print(f)

_init('./instances/nug12.dat')
_print()
init("./instances/tai100a.dat")
_print()
