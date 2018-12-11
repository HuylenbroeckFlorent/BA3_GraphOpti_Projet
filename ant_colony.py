from __future__ import division

from read_QAP import read_QAP

size=0
D=[]
F=[]

def init(path):
	global size,D,F
	size,D,F=read_QAP(path)

def ant(alpha, beta):
	return

def compute_probability(alpha,beta,s,elements):
	return

def visibility(e1,e2):
	return 1/D[e1][e2]

def ant_colony(N,alpha,beta,Q,omega):
	return

def drop_pheromones(s,Q):
	return

def evaporate_pheromone(omega):
	return

init('./instances/nug12.dat')