from __future__ import division

from threading import Thread
import numpy as np
import numpy.random as np_random

class ant(Thread):
	def __init__(self, alpha, beta, Q, permutation, pheromones, swap_cost_function):
		Thread.__init__(self)
		self.alpha=alpha
		self.beta=beta
		self.Q=Q
		self.permutation=permutation
		self.pheromones=pheromones
		self.swap_cost_function=swap_cost_function

		self.size=len(permutation)
		self.R=int(self.size/3)

		self.local_search(self.permutation)
		return

	def run(self):
		for i in range(self.R):
			s=np_random.choice(range(self.size))
			probs=self.compute_probability(self.permutation[s])
			#print(probs)
			r=np_random.choice(range(self.size),p=probs)
			self.swap_by_indexes(r,s)
			#print(self.permutation)
			self.local_search(self.permutation)
			#print(self.permutation)
			#self.drop_pheromones(self.permutation,self.Q)
			i+=i
		return

	def compute_probability(self,s):
		prob=np.zeros(self.size)
		for element in self.permutation:
			if element==s:
				continue
			prob[element]=self.pheromones[s][self.permutation[element]]+self.pheromones[element][self.permutation[s]]
		prob/=sum(prob)
		return prob

	def visibility(e1,e2):
		return 1/D[e1][e2]

	def local_search(self,permutation):
		for reps in range(2):
			for i in np_random.permutation(range(self.size)):
				for j in np_random.permutation(range(self.size)):
					if j==i:
						continue
					if self.swap_cost_function(permutation,i,j)<0:
						self.swap_by_indexes(i,j)
			reps+=1
		return permutation

	def swap_by_indexes(self,i,j):
		tmp=self.permutation[i]
		self.permutation[i]=self.permutation[j]
		self.permutation[j]=tmp