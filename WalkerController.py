import breve
from Genome import Genome
class WalkerController( breve.Object ):

	def __init__( self, chromosomes = None):
		self.walkerBody = None
		breve.Object.__init__( self )
		self.distanceTraveled = 0
		self.uprightRatio = 0
		self.score = 0
		self.ID = -1
		self.colors = [breve.randomExpression( breve.vector( 1, 1, 1 ) ), breve.randomExpression( breve.vector( 1, 1, 1 ) )]
		self.initGenome( chromosomes )

	def applyJointVelocities( self, t ):
		self.walkerBody.setJointVelocities(self.genome.calculateJointVelocities(t))

	def breedWith( self, other):
		return self.getGenome().crossover( other.getGenome() )

	def setupBody( self ):
		self.walkerBody.initBody( self.getChromosomes() )
		self.walkerBody.center()
		self.walkerBody.setColors( self.getColors() )

	def deleteBody( self ):
		self.walkerBody.deleteBody()

	def getBody( self ):
		return self.walkerBody

	def getColors( self ):
		return self.colors

	def getDistance( self ):
		return self.distanceTraveled
	
	def getLocation( self ):
		return walkerBody.getLocation()

	def mutate( self ):
		self.genome.mutate()
	
	def getGenome( self ):
		return self.genome

	def setGenome( self, chromosomes ):
		self.genome.setChromosomes( chromosomes )

	def getGenomeString( self ):
		return self.genome.toString()

	def getID( self ):
		return self.ID

	def setID( self, n ):
		self.ID = n

	def getLocation( self ):
		return self.walkerBody.getLocation()

	def isUpright( self ):
		return self.walkerBody.isUpright()

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


