import breve
import math
from random import randint, uniform
from Genome import Genome

# The genome consists of 3 DT per leg (= 12) +  angV + max amplitude + body width + two leg lengths (upper and lower) + footWidth  = 18 values

PI = 3.14159

ANGV = 12
AMPLITUDE = 13
BODY_WIDTH = 14
UPPER_LEG_LENGTH = 15
LOWER_LEG_LENGTH = 16
FOOT_WIDTH = 17

# Values for initialization:
MAX_ANGV = 10.0
MAX_AMPLITDUE = 10.0
MIN_BODY_WIDTH = 4.0
MAX_BODY_WIDTH = 8.0
MIN_LEG_LENGTH = 0.5
MAX_LEG_LENGTH = 2.0
MIN_FOOT_WIDTH = 0.7
MAX_FOOT_WIDTH = 1.5

class FourLeggedWalkerGenome( Genome ):
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

	def randomize( self ):
		for i in range(0,12):
			self.chromosomes[ i ] = uniform( -PI, PI )
		self.chromosomes[ ANGV ] = uniform( -MAX_ANGV, MAX_ANGV )	
		self.chromosomes[ AMPLITUDE ] = uniform( 0, MAX_AMPLITDUE )	
		self.chromosomes[ BODY_WIDTH ] = uniform( MIN_BODY_WIDTH, MAX_BODY_WIDTH )
		self.chromosomes[ UPPER_LEG_LENGTH ] = uniform( MIN_LEG_LENGTH, MAX_LEG_LENGTH )
		self.chromosomes[ LOWER_LEG_LENGTH ] = uniform( MIN_LEG_LENGTH, MAX_LEG_LENGTH )
		self.chromosomes[ FOOT_WIDTH ] = uniform( MIN_FOOT_WIDTH, MAX_FOOT_WIDTH )