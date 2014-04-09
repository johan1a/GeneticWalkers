import breve
from Genome import Genome
class WalkerController( breve.Object ):
	def __init__( self ):
		breve.Object.__init__( self )
		self.distanceTraveled = 0
		self.ID = -1
		self.genome = Genome()
		self.colors = [breve.randomExpression( breve.vector( 1, 1, 1 ) ),breve.randomExpression( breve.vector( 1, 1, 1 ) )]

	def breedWith( self, other):
		child = WalkerController()
		child.getGenome().crossover( other.getGenome(), self.getGenome() )
		return child

	def applyJointVelocities( self, walkerBody, t ):
		walkerBody.setJointVelocities(self.genome.calculateJointVelocities(t))

	def getColors( self ):
		return self.colors

	def getDistance( self ):
		return self.distanceTraveled

	def mutate( self ):
		self.genome.mutate()

	def getGenome( self ):
		return self.genome

	def getID( self ):
		return self.ID

	def randomize( self ):
		self.genome.randomize()

	def setDistanceTraveled( self, value ):
		self.distanceTraveled = value

	def setID( self, n ):
		self.ID = n

	def getGenomeString( self ):
		return self.genome.toString()