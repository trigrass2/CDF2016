#!/usr/bin/python3.4

import math
import random

def f(x):
	return 1.0/(1.0+math.exp(-x))

alpha = 0.1
seuil = 0.05

class NeuralNet:
	def __init__(self,t_couches):
		nb_couches = len(t_couches)

		self.nbc = nb_couches
		self.length = t_couches
		self.neurone = []
		self.w = []

		for i in range(0,nb_couches):
			if i != (nb_couches-1):
				self.neurone += [-1]
			for j in range(0,t_couches[i]):
				self.neurone += [0]

		for i in range(0,t_couches[0]+1):
			for j in range(0,t_couches[1]):
				(self.w).append(random.uniform(-1,1))

		for i in range(1,nb_couches-1):
			for j in range(0,t_couches[i]+1):
				for k in range(0,t_couches[i+1]):
					(self.w).append(random.uniform(-1,1))

			
	#private methods
	def __sum__(self,i,j):
		if i <= 1:
			print('Rien n\'est relie a la couche entree...')
		elif j <= 0:
			print('Rien n\'est relie au neurone seuil...')
		else:
			#res=[(x,w)]
			res = []
			tup = [0,0]
			sum_pond = 0.0

			(first_n,last_n) = self.index_couche(i-1)
			for k in range(0,self.length[i-2]+1):
				tup[0] = self.neurone[first_n+k]
				
				(first_w,last_w) = self.index_poids(i-1,k)
				tup[1] = self.w[first_w+(j-1)]

				res.append((tup[0],tup[1]))
		
			for tup in res:
				sum_pond += tup[1]*tup[0]

			return sum_pond
	
	#public methods	
	def index_couche(self,n):
		ind = 0

		for i in range(0,n-1):
			ind += self.length[i]+1

		if n == self.nbc:
			return (ind,ind+self.length[n-1])
		else:	
			return (ind,ind+self.length[n-1]+1)

	def indice_neurone(self,i,j):
		(first_n,last_n) = self.index_couche(i)
		if i == self.nbc:
			return (first_n+(j-1))
		else:
			return (first_n+j)

	def index_poids(self,i,j):
		#i <= self.nbc-1
		ind = 0
		for k in range(0,i-1):
			ind += (self.length[k]+1)*(self.length[k+1])
		for k in range(0,j):
			ind += self.length[i]

		return (ind,ind+self.length[i])

	def print_r(self):
		(first_n,last_n) = self.index_couche(self.nbc)
		print(self.neurone[first_n:last_n])

	def calc(self,data_in,f):
		if len(data_in) != self.length[0]:
			print('Erreur dans la taille du vecteur d\'entree')
		else:
			#on entre dans la premiere couche le vecteur initial
			for i in range(1,self.length[0]+1):
				self.neurone[i] = data_in[i-1]

			for i in range(2,self.nbc+1):
				for j in range(0,self.length[i-1]):
					self.neurone[self.indice_neurone(i,j+1)] = f(self.__sum__(i,j+1))
	
	def learn(self,X,Y,f,alpha,seuil):
		finished = False
		compteur = 0

		while not finished and compteur <= 1000:
			finished = True
			cmpt = 0

			for i in range(0,len(X)):
				self.calc(X[i],f)
				d = []
				error = 0.0
				
				(first_n,last_n) = self.index_couche(self.nbc)
				out_vect = self.neurone[first_n:last_n]
				targ_vect = Y[i]

				for j in range(0,self.length[self.nbc-1]):
					error += (targ_vect[j]-out_vect[j])**2
				error /= 2

				if error >= seuil:
					cmpt += 1
					finished = False
				
				#print error

				d.append([])
				for j in range(0,self.length[self.nbc-1]):
					(d[0]).append(out_vect[j]*(1.0-out_vect[j])*(targ_vect[j]-out_vect[j]))

				for c in range(self.nbc-1,1,-1):
					d.append([])
					#on ne calcule pas les di pour les neurones seuils
					for j in range(1,self.length[c-1]+1):
						sum_fact = 0.0
						(first_n,last_n) = self.index_poids(c,j)
						weight = self.w[first_n:last_n]

						for k in range(0,self.length[c]):
							sum_fact += d[-2][k]*weight[k]

						out = self.neurone[self.indice_neurone(c,j)]
						(d[-1]).append(out*(1-out)*sum_fact)
				 
				for j in range(1,self.nbc):
					(first_n,last_n) = self.index_couche(j)
					for k in range(0,last_n-first_n):
						(first_w,last_w) = self.index_poids(j,k)
						for l in range(first_w,last_w):
							self.w[l] += alpha*self.neurone[self.indice_neurone(j,k)]*d[-j][l-first_w]
			compteur += 1 
			#print('-----------------',cmpt)


if __name__ == '__main__':
	NN = NeuralNet([5,5,1])

	V = []
	S = []

	for i in range(0,10):
		V.append([random.uniform(0,1) for s in range(0,5)])
		S.append([1])
	for i in range(0,10):
		V.append([random.uniform(0,1) for s in range(0,5)])
		S.append([0])

	NN.learn(V,S,f,alpha,seuil)
	NN.calc([0.2,0.1,0.2,0.1,0.1],f)
	NN.print_r()
	print(NN.w[:10])
