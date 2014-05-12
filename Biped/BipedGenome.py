import breve
import math
from random import randint, uniform
from Genome import Genome

# The genome consists of 3 DT + 3 amplitude + angV = 7 values

PI = 3.14159

AMPLITUDE = 3
ANGV = 6

# Values for initialization:
MAX_ANGV = 1
MAX_AMPLITDUE = 1

class BipedGenome( Genome ):
	def __init__( self, chromosomes = None ):
		breve.Object.__init__( self )
		if(chromosomes is None):
			self.chromosomes = [ 0 ] * 7
			self.randomize()
		else:
			self.chromosomes = chromosomes

	def calculateJointVelocities( self, time ):
		return [self.calculateJointVelocity( i, time ) for i in range( 0, 6 )]

	def calculateJointVelocity( self, i, time ):
		return self.getAmplitude( i ) *  math.sin( self.chromosomes[ ANGV ] * time + self.getDT( i ) ) 

	def getAmplitude( self, i ):
		return self.chromosomes[ AMPLITUDE + i // 2 ]

	def getDT( self, i ):
		if( i % 2 == 0):
			return self.chromosomes[ i ]
		else:
			return self.chromosomes[ i - 1 ] + PI / 2

	def randomize( self ):
		for i in range(0,3):
			self.chromosomes[ i ] = uniform( -PI, PI )
		for i in range(3,6):
			self.chromosomes[ i ] = uniform( 0, MAX_AMPLITDUE )
		self.chromosomes[ ANGV ] = uniform( -MAX_ANGV, MAX_ANGV )

	def getType( self ):
		return "Biped"