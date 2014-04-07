import breve
import math
from random import randint, uniform

PI = 3.14159
MUTATION_PROBABILITY = 0.05
MAX_ANGV = 2.5

ANGV = 8
AMPLITUDE = 9
class Genome( breve.Object ):
	def __init__( self ):
		breve.Object.__init__( self )
		self.genes = [ 0 ] * 10
		self.randomize()

	def calculateJointVelocities( self, time ):
		return [self.calculateJointVelocity(i, time ) for i in range(0,8)]

	def calculateJointVelocity( self, i, time ):
		return self.getAmplitude() * ( math.sin( self.getAngV(i) * ( time + self.getDT(i) )) - 0 ) 

	def getAmplitude( self ):
		return self.genes[ AMPLITUDE ]

	def getAngV( self, i ):
		return self.genes[ ANGV ]

	def getDT( self, i ):
		return self.genes[ i ] 

	def crossover( self, p1, p2 ):
		if randint( 0, 1 ):
			tmp = p2
			p2 = p1
			p1 = tmp

		crossoverPoint = randint(0, len(self.genes) - 1 )

		g1 = p1.getGenes()
		g2 = p2.getGenes()
		self.genes = g1[:crossoverPoint] + g2[crossoverPoint:]


	def getGenes( self ):
		return self.genes

	def mutate( self ):
		for n in range(0,8):
			k = uniform(0,1)
			if (k < MUTATION_PROBABILITY ):
				if n < ANGV:
					self.genes[ n ] = uniform(-PI, PI)
				if n == ANGV:
					self.genes[ n ] = self.genes[ n ] * uniform(0.8, 1.2)
				if n == AMPLITUDE:
					self.genes[ n ] = self.genes[ n ] * uniform(0.8, 1.2)
				print '''mutated item %s of %s''' % (  n, self )

	def randomize( self ):
		for i in range(0,8):
			self.genes[ i ] = uniform( -MAX_ANGV, MAX_ANGV  )
		self.genes[ ANGV ] = uniform(-PI, PI)	
		self.genes[ AMPLITUDE ] = uniform(4, 6)	