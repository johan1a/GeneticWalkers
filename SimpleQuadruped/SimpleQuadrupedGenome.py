import breve
import math
from random import randint, uniform
from Genome import Genome

# The genome consists of 2 DT per leg ( = 8) + angV + amplitude = 10 values

PI = 3.14159

ANGV = 8
AMPLITUDE = 9

# Values for initialization:
MAX_ANGV = 18.0
MAX_AMPLITDUE = 12.0

class SimpleQuadrupedGenome( Genome ):
	def __init__( self, chromosomes = None ):
		breve.Object.__init__( self )
		if(chromosomes is None):
			self.chromosomes = [ 0 ] * 10
			self.randomize()
		else:
			self.chromosomes = chromosomes

	def calculateJointVelocities( self, time ):
		return [ self.calculateJointVelocity( i, time ) for i in range( 0, 8 ) ]

	def calculateJointVelocity( self, i, time ):
		return self.chromosomes[ AMPLITUDE ] *  math.sin( self.chromosomes[ ANGV ] * time + self.getDT(i) ) 

	def getDT( self, i ):
		return self.chromosomes[ i ]

	def randomize( self ):
		for i in range(0,8):
			self.chromosomes[ i ] = uniform( -PI, PI )
		self.chromosomes[ ANGV ] = uniform( -MAX_ANGV, MAX_ANGV )	
		self.chromosomes[ AMPLITUDE ] = uniform( 0, MAX_AMPLITDUE )	

	def getType( self ):
		return "SimpleQuadruped"