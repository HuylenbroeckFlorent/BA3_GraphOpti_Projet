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

		self.size=len(self.permutation)
		self.R=int(self.size/3)
		self.q=0.9

		if not first:
			self.local_search(self.permutation)
		return

	def run(self):
		prev_permutation=deepcopy(self.permutation)
		prev_cost=self.cost_function(self.permutation)
		for _ in range(self.R):
			self.pheromone_trail_swaps()
			self.local_search(self.permutation)
		if self.intensification and prev_cost<self.cost_function(self.permutation):
			self.permutation=prev_permutation
		return

	def pheromone_trail_swaps(self):
		r=np_random.choice(range(self.size))
		probs=self.compute_probability(self.permutation[r])
		if np_random.choice([True,False],p=[self.q,(1-self.q)]):
			s=np.argmax(probs)
		else:
			s=np_random.choice(range(self.size),p=probs)
		swap_by_indexes(self.permutation,r,s)
		return

	def compute_probability(self,r):
		probs=np.zeros(self.size)
		for element in self.permutation:
			if element==r:
				continue
			else:
				probs[element]=self.pheromones[r][self.permutation[element]]+self.pheromones[element][self.permutation[r]]
		probs/=sum(probs)
		return probs