import breve
import math
from random import randint, uniform

MUTATION_PROBABILITY = 0.05

class Genome( breve.Object ):

	def crossover( self, otherParent ):
		p1 = self
		p2 = otherParent

		if randint( 0, 1 ):
			tmp = p2
			p2 = p1
			p1 = tmp

		crossoverPoint = randint(0, len( self.chromosomes ) - 1 )

		g1 = p1.getChromosomes()
		g2 = p2.getChromosomes()
		return [ g1[:crossoverPoint] + g2[crossoverPoint:], g2[:crossoverPoint] + g1[crossoverPoint:] ]

	def getChromosomes( self ):
		return self.chromosomes

	def mutate( self ):
		for n in range(0,10):
			k = uniform(0,1)
			if (k < MUTATION_PROBABILITY ):
					self.chromosomes[ n ] = self.chromosomes[ n ] * uniform(0.9, 1.1)

	def toString( self ):
		return " ".join([str(g) for g in self.chromosomes])
