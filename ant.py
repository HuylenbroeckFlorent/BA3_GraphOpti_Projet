from __future__ import division

from threading import Thread
import numpy as np
import numpy.random as np_random
from copy import deepcopy

from ant_util import swap_by_indexes

#TODO document this shit
class ant(Thread):
	def __init__(self, permutation, pheromones, cost_function, local_search, intensification, first):
		Thread.__init__(self)
		self.permutation=permutation
		self.pheromones=pheromones
		self.cost_function=cost_function
		self.local_search=local_search
		self.intensification=intensification

		self.size=len(permutation)
		self.R=int(self.size/3)
		self.q=0.9

		if not first:
			self.local_search(self.permutation)
		return

	def run(self):
		prev_permutation=deepcopy(self.permutation)
		prev_cost=self.cost_function(self.permutation)
		for i in range(self.R):
			self.pheromone_trail_swaps()
			self.local_search(self.permutation)
			i+=i
		if self.intensification and prev_cost<self.cost_function(self.permutation):
			self.permutation=prev_permutation
		return

	def pheromone_trail_swaps(self):
		s=np_random.choice(range(self.size))
		probs=self.compute_probability(self.permutation[s])
		if np_random.choice([True,False],p=[self.q,(1-self.q)]):
			r=np.argmax(probs)
		else:
			r=np_random.choice(range(self.size),p=probs)
		swap_by_indexes(self.permutation,s,r)
		return

	def compute_probability(self,s):
		probs=np.zeros(self.size)
		for element in self.permutation:
			if element==s:
				continue
			probs[element]=self.pheromones[s][self.permutation[element]]+self.pheromones[element][self.permutation[s]]
		probs/=sum(probs)
		return probs