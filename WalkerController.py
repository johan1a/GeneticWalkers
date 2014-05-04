import breve
from Genome import Genome
class WalkerController( breve.Object ):

	def __init__( self, genome = None):
		breve.Object.__init__( self )
		self.distanceTraveled = 0
		self.uprightRatio = 0
		self.score = 0

		self.ID = -1
		self.genome = Genome( genome )
		self.colors = [breve.randomExpression( breve.vector( 1, 1, 1 ) ), breve.randomExpression( breve.vector( 1, 1, 1 ) )]

	def breedWith( self, other):
		return self.getGenome().crossover( other.getGenome() )

	def applyJointVelocities( self, walkerBody, t ):
		walkerBody.setJointVelocities(self.genome.calculateJointVelocities(t))

	def getChromosomes( self ):
		return self.genome.getChromosomes()

	def getColors( self ):
		return self.colors

	def getDistance( self ):
		return self.distanceTraveled

	def mutate( self ):
		self.genome.mutate()
	
	def setGenome( self, chromosomes ):
		self.genome.setChromosomes( chromosomes )

	def getGenome( self ):
		return self.genome

	def getID( self ):
		return self.ID

	def randomize( self ):
		self.getGenome().randomize()

	def setDistanceTraveled( self, value ):
		self.distanceTraveled = value

	def setUprightRatio( self, value ):
		self.uprightRatio = value

	def getScore( self ):
		return self.score

	def setScore( self, value ):
		self.score = value

	def setID( self, n ):
		self.ID = n

	def getGenomeString( self ):
		return self.genome.toString()