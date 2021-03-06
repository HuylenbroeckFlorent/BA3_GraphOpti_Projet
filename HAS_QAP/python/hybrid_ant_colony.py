from __future__ import division

import sys
import time 
from util import read_QAP, swap_by_indexes

from copy import deepcopy
import numpy as np
import numpy.random as np_random

#Needed for importing read_QAP
sys.path.append('../util')
from util import read_QAP, swap_by_indexes
from ant import ant

#sys.tracebacklimit=0

def open(path):
	global size,distances,flows
	size,distances,flows=read_QAP(path)

def reinitialize():
	#Generate N-1 random permutations and apply a local search on them
	global permutations, all_time_best_permutation
	permutations=[local_search(permutation) for permutation in generate_permutations(N-1)]
	permutations.append(all_time_best_permutation)

	#Reinitialize pheromones
	init_pheromones()

	#Reset intensification trigger
	global intensification
	intensification=True

	#Reset diversification_trigger 
	global diversification_trigger
	diversification_trigger=0

	#Boolean for constructing ants purpose
	global diversification_happened_this_iteration
	diversification_happened_this_iteration=True

#Generates inital permutations for every ants
def generate_permutations(N):
	permutations=[]
	for i in range(N):
		permutations.append(np_random.permutation(size))
	return permutations

#Cost function for the solution s
def cost_function(s):
	cost=0
	for i in range(size):
		for j in range(size):
			cost+=distances[i][j]*flows[s[i]][s[j]]
	return cost

#Shift in cost if we swap i an j in solution s
def swap_cost_function(s,i,j):
	cost=0
	cost=(distances[i][i]-distances[j][j])*(flows[s[j]][s[j]]-flows[s[i]][s[i]])+(distances[i][j]-distances[j][i])*(flows[s[j]][s[i]]-flows[s[i]][s[j]])
	for k in range(len(s)):
		if k==j or k==i:
			continue
		cost+=(distances[k][i]-distances[k][j])*(flows[s[k]][s[j]]-flows[s[k]][s[i]])+(distances[i][k]-distances[j][k])*(flows[s[j]][s[k]]-flows[s[i]][s[k]])
	return cost

#Local search function for a solution s
def local_search(s):
	initial_s=deepcopy(s)
	for _ in range(2):
		for i in np_random.permutation(range(size)):
			for j in np_random.permutation(range(size)):
				if j==i:
					continue
				if swap_cost_function(s,i,j)<0:
					swap_by_indexes(s,i,j)
		if np.array_equal(initial_s,s):
			return s
	return s

def init_pheromones():
	global pheromones, all_time_best_permutation
	pheromones=np.ones((size,size))*(1/(Q*cost_function(all_time_best_permutation)))


def evaporate_pheromone():
	global pheromones
	pheromones=(1-q)*pheromones
	return

#Drop pheromones according to solution s
def drop_pheromones(s):
		global pheromones
		cost=cost_function(s)
		for i in range(len(s)):
			pheromones[i][s[i]]+=0.1/cost

# ---------- INIT ----------

#Launching the timer
time.clock()

#size of the QAP
size=0

#Distances matrix
distances=[]

#Flows matrix
flows=[]

#Chosen number of ants
N=10

#Parameter for pheromones initialization
Q=100

#Evaporation coeficient
q=0.1

#Checking for arguments
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

#Max number of iteration without improving current best solution, current counter, and a boolean to reset ants
diversification_trigger_max=int(size/2)
diversification_trigger=0
diversification_happened_this_iteration=False

#Generate N random permutations and apply a local search on them
permutations=[local_search(permutation) for permutation in generate_permutations(N)]

#Best solution found so far
all_time_best_permutation=deepcopy(min(permutations,key=cost_function))

#Solutions found by previous iteration (only for comparing as a whole, so keeping the sum is easier and faster)
previous_solutions=np.inf

#Initialize pheromones
init_pheromones()

#Intensification trigger
intensification=True

#Initialze first ants
ants=[]
for permutation in permutations:
	ants.append(ant(permutation,pheromones,cost_function,local_search, intensification, first=True))

#What time has elapsed so far, used to make sure not to use too much time in main loop
t_1=time.clock()

# ---------- MAIN LOOP ----------
while time.clock()<max_time-t_1:

	#Start run() in ants
	for _ant in ants:
		_ant.start()

	#Wait for every ants to finish computing
	for _ant in ants:
		_ant.join()

	#Get every ant's solution and find the best one
	permutations=[_ant.permutation for _ant in ants]
	iteration_best_permutation=deepcopy(min(permutations,key=cost_function))

	#Trigger intensification if best solution has been improved
	if cost_function(all_time_best_permutation)>cost_function(iteration_best_permutation):
		diversification_trigger=0
		if not intensification:
			print('intensification ON')
			intensification=True
	else:
		diversification_trigger+=1

	#Un-trigger intensification if no ant has improved it's solution (checked by comparing sums of solutions)
	if intensification and sum([cost_function(permutation) for permutation in permutations])==previous_solutions:
		print('intensification OFF')
		intensification=False

	#Update previous solutions sum
	previous_solutions=sum([cost_function(permutation) for permutation in permutations])

	#Update all time best solution
	all_time_best_permutation=deepcopy(min(all_time_best_permutation,iteration_best_permutation, key=cost_function))

	#Evaporate pheromones
	evaporate_pheromone()

	#Drop pheromones on the current best solution
	drop_pheromones(all_time_best_permutation)

	#Trigger diversification mecanism if needed
	if diversification_trigger==diversification_trigger_max:
		print('diversification')
		reinitialize()

	print(all_time_best_permutation,' - iteration best : ',cost_function(iteration_best_permutation),' - all time best : ',cost_function(all_time_best_permutation))

	#Re-initialize ants for next iteration
	ants=[]
	for permutation in permutations:
		ants.append(ant(permutation,pheromones,cost_function,local_search, intensification, diversification_happened_this_iteration))

	diversification_happened_this_iteration=False

print('\n==========\n\nTIME DONE : ',int(time.clock()+t_1),'s\nBEST SOLUTION FOUND : ',[i+1 for i in all_time_best_permutation],'\nCOST : ',cost_function(all_time_best_permutation),'\n\n==========')
