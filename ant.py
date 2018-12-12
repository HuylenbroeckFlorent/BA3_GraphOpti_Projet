from threading import Thread
import numpy as np
import numpy.random as np_random

class ant(Thread):
	def __init__(self, alpha, beta, permutation, pheromones):
		self.alpha=alpha
		self.beta=beta
		self.permutation=permutation
		self.pheromones=pheromones

		self.size=len(permutation)
		self.R=int(self.size/3)
		return

	def run(self):
		for i in range(self.R):
			s=np_random.choice(range(self.size))
			probs=self.compute_probability(self.permutation[s])
			print(probs)
			r=np_random.choice(range(self.size),p=probs)
			tmp=self.permutation[s]
			self.permutation[s]=self.permutation[r]
			self.permutation[r]=tmp
			print(self.permutation)
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

	def drop_pheromones(s,Q):
		return