from __future__ import division

import sys
import time

import numpy as np
import numpy.random as np_random
from threading import Thread

from read_QAP import read_QAP

#sys.tracebacklimit=0

def open(path):
	global size,distances,flows
	size,distances,flows=read_QAP(path)

def generate_permutations(N):
	permutation=[]
	for i in range(N):
		permutation.append(np_random.permutation(size))
	return permutation

def cost_function(s):
	cost=0
	for i in range(size):
		for j in range(size):
			cost+=distances[i][j]*flows[s[i]][s[j]]
	return cost

def evaporate_pheromone(omega):
	return

size=0
distances=[]
flows=[]
N=10
Q=100

time.clock()
if len(sys.argv)<3:
	raise ValueError("ant_colony must be fed at least one argument :\n - path : the relative or absolute path to the .dat file describing the QAP\n - (OPTIONAL) maxtime : max computation time (in seconds), default=60")
	sys.exit(0)

else:
	if len(sys.argv)>1:
		open(sys.argv[1])
	if len(sys.argv)>2:
		max_time=float(sys.argv[2])
	else:
		max_time=1.0

permutations=generate_permutations(N)
current_min_cost=min([cost_function(perm) for perm in permutations])

pheromones=np.ones((size,size))*(1/Q*current_min_cost)

t_1=time.clock()

#Make sure we're still within allocated time
while time.clock()<max_time-t_1:
	x=2


class ant(Thread):
	def __init__(self, alpha, beta, permutation):
		self.alpha=alpha
		self.beta=beta
		self.permutation=permutation
		return

	def compute_probability(alpha,beta,current_location,other_location):

		return

	def visibility(e1,e2):
		return 1/D[e1][e2]

	def drop_pheromones(s,Q):
		return