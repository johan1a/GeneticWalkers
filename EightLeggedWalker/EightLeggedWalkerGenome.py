import breve
import math
from random import randint, uniform
from Genome import Genome

# The genome consists of 1 DT per 2 legs (= 4) +  angV + max amplitude = 6 values

PI = 3.14159

ANGV = 4
AMPLITUDE = 5

# Values for initialization:
MAX_ANGV = 14.0
MAX_AMPLITDUE = 10.0

class EightLeggedWalkerGenome( Genome ):
	def __init__( self, chromosomes = None ):
		breve.Object.__init__( self )
		if(chromosomes is None):
			self.chromosomes = [ 0 ] * 18
			self.randomize()
		else:
			self.chromosomes = chromosomes

	def calculateJointVelocities( self, time ):
		return [self.calculateJointVelocity( i, time ) for i in range( 0, 8 )]

	def calculateJointVelocity( self, i, time ):
		return self.chromosomes[ AMPLITUDE ] *  math.sin( self.chromosomes[ ANGV ] * time + self.getDT(i) ) 

	def getDT( self, i ):
		return self.chromosomes[ i % 4 ] 

	def randomize( self ):
		for i in range(0,4):
			self.chromosomes[ i ] = uniform( -PI, PI )
		self.chromosomes[ ANGV ] = uniform( -MAX_ANGV, MAX_ANGV )	
		self.chromosomes[ AMPLITUDE ] = uniform( 0, MAX_AMPLITDUE )	

	def getType( self ):
		return "FourLegged"