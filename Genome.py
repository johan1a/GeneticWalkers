import breve
import math
from random import randint, uniform


# The genome consists of 3 DT per leg (= 12) +  angV + max amplitude + body width + two leg lengths (upper and lower) + footWidth  = 18 values


PI = 3.14159
MUTATION_PROBABILITY = 0.05

ANGV = 12
AMPLITUDE = 13
BODY_WIDTH = 14
UPPER_LEG_LENGTH = 15
LOWER_LEG_LENGTH = 16
FOOT_WIDTH = 17

# Values for initialization:
MAX_ANGV = 10.0
MAX_AMPLITDUE = 10.0
MIN_BODY_WIDTH = 2.0
MAX_BODY_WIDTH = 6.0
MIN_LEG_LENGTH = 0.5
MAX_LEG_LENGTH = 2.0
MIN_FOOT_WIDTH = 0.4
MAX_FOOT_WIDTH = 1.5

class Genome( breve.Object ):
	def __init__( self, chromosomes = None ):
		breve.Object.__init__( self )
		if(chromosomes is None):
			self.chromosomes = [ 0 ] * 18
			self.randomize()
		else:
			self.chromosomes = chromosomes

	def calculateJointVelocities( self, time ):
		return [self.calculateJointVelocity( i, time ) for i in range( 0, 12 )]

	def calculateJointVelocity( self, i, time ):
		return self.getAmplitude() *  math.sin( self.getAngV() * time + self.getDT(i) ) 

	def getAmplitude( self ):
		return self.chromosomes[ AMPLITUDE ]

	def getAngV( self ):
		return self.chromosomes[ ANGV ]

	def getDT( self, i ):
		return self.chromosomes[ i ] 

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
				if n < ANGV: # a joint time delay
					self.chromosomes[ n ] = uniform(-PI, PI)
				elif n == ANGV: 
					self.chromosomes[ n ] = self.chromosomes[ n ] * uniform(0.8, 1.2)
				elif n == AMPLITUDE: 
					self.chromosomes[ n ] = self.chromosomes[ n ] * uniform(0.7, 1.3)
				elif n == BODY_WIDTH:
					self.chromosomes[ n ] = self.chromosomes[ n ] * uniform(0.9, 1.1)
				elif n == UPPER_LEG_LENGTH:
					self.chromosomes[ n ] = self.chromosomes[ n ] * uniform(0.8, 1.2)
				elif n == LOWER_LEG_LENGTH:
					self.chromosomes[ n ] = self.chromosomes[ n ] * uniform(0.8, 1.2)
				elif n == FOOT_WIDTH:
					self.chromosomes[ n ] = self.chromosomes[ n ] * uniform(0.9, 1.1)

	def randomize( self ):
		for i in range(0,12):
			self.chromosomes[ i ] = uniform( -PI, PI )
		self.chromosomes[ ANGV ] = uniform( -MAX_ANGV, MAX_ANGV )	
		self.chromosomes[ AMPLITUDE ] = uniform( 0, MAX_AMPLITDUE )	
		self.chromosomes[ BODY_WIDTH ] = uniform( MIN_BODY_WIDTH, MAX_BODY_WIDTH )
		self.chromosomes[ UPPER_LEG_LENGTH ] = uniform( MIN_LEG_LENGTH, MAX_LEG_LENGTH )
		self.chromosomes[ LOWER_LEG_LENGTH ] = uniform( MIN_LEG_LENGTH, MAX_LEG_LENGTH )
		self.chromosomes[ FOOT_WIDTH ] = uniform( MIN_FOOT_WIDTH, MAX_FOOT_WIDTH )

	def setChromosomes( self, chromosomes ):
		self.chromosomes = chromosomes

	def toString( self ):
		return " ".join([str(g) for g in self.chromosomes])
