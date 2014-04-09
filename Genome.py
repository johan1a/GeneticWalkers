import breve
import math
from random import randint, uniform

PI = 3.14159
MUTATION_PROBABILITY = 0.05
MAX_ANGV = 5

ANGV = 8
AMPLITUDE = 9
class Genome( breve.Object ):
	def __init__( self ):
		breve.Object.__init__( self )
		self.chromosomes = [ 0 ] * 10
		self.randomize()

	def calculateJointVelocities( self, time ):
		return [self.calculateJointVelocity( i, time ) for i in range(0,8)]

	def calculateJointVelocity( self, i, time ):
		return self.getAmplitude() *  math.sin( self.getAngV() * time + self.getDT(i) ) 

	def getAmplitude( self ):
		return self.chromosomes[ AMPLITUDE ]

	def getAngV( self ):
		return self.chromosomes[ ANGV ]

	def getDT( self, i ):
		return self.chromosomes[ i ] 

	def crossover( self, p1, p2 ):
		if randint( 0, 1 ):
			tmp = p2
			p2 = p1
			p1 = tmp

		crossoverPoint = randint(0, len(self.chromosomes) - 1 )

		g1 = p1.getchromosomes()
		g2 = p2.getchromosomes()
		self.chromosomes = g1[:crossoverPoint] + g2[crossoverPoint:]

	def getchromosomes( self ):
		return self.chromosomes

	def mutate( self ):
		for n in range(0,10):
			k = uniform(0,1)
			if (k < MUTATION_PROBABILITY ):
				if n < ANGV:
					self.chromosomes[ n ] = uniform(-PI, PI)
				if n == ANGV:
					self.chromosomes[ n ] = self.chromosomes[ n ] * uniform(0.7, 1.3)
				if n == AMPLITUDE:
					self.chromosomes[ n ] = self.chromosomes[ n ] * uniform(0.7, 1.3)
					
	def randomize( self ):
		for i in range(0,8):
			self.chromosomes[ i ] = uniform( -MAX_ANGV, MAX_ANGV  )
		self.chromosomes[ ANGV ] = uniform(-MAX_ANGV, MAX_ANGV)	
		self.chromosomes[ AMPLITUDE ] = uniform(4, 6)	

	def setChromosomes( self, chromosomes ):
		self.chromosomes = chromosomes

	def toString( self ):
		return " ".join([str(g) for g in self.chromosomes])
