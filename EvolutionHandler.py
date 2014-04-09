import breve
import sys
print sys.version
from WalkerBody import WalkerBody
from WalkerController import WalkerController
from Genome import Genome
from random import randint

breve.Genome = Genome # takes care of problems with import conflicts in other files 

ROUND_MAX_DURATION = 60
STATUS_CHECK_INTERVAL = 10
POPULATION_SIZE = 30
ELITE_COUNT = 5
SAVED_WALKERS = "savedWalkers.txt"

# A walker is considered stationary if it has not moved 
# further than MOVEMENT_THRESHOLD since the last status check.
MOVEMENT_THRESHOLD = 1 

class EvolutionHandler( breve.PhysicalControl ):
	def __init__( self ):
		breve.PhysicalControl.__init__( self )
		self.initWorld()
		self.initWalkers()
		self.startNewTournament()

	def startNewTournament( self ):
		self.currentWalkerIndex = -1
		self.initWalkerIDs()
		self.startNewRound()

	def startNewRound( self ):
		self.currentWalkerIndex = self.currentWalkerIndex + 1
		self.roundDuration = 0;
		self.walkerBody.center()
		self.walkerBody.setColors(self.walkers[ self.currentWalkerIndex ].getColors())
		self.walkerPrevLocation = self.walkerBody.getLocation()
		self.showInfo()
		self.schedule( 'checkWalkerStatus', ( self.getTime() + STATUS_CHECK_INTERVAL ) )

	# Checks if the walker has run out of time or stopped.
	# Switches to the next walker if that is the case.
	def checkWalkerStatus( self ):
		self.roundDuration = self.roundDuration + STATUS_CHECK_INTERVAL
		if( self.walkerIsStill() or self.roundDuration >= ROUND_MAX_DURATION): #self.walkerIsStill() || 
			self.switchWalker()
		else:
			self.schedule( 'checkWalkerStatus', ( self.getTime() + STATUS_CHECK_INTERVAL ) )
			self.walkerPrevLocation = self.walkerBody.getLocation()

	def switchWalker( self ):
		distance = breve.length( self.walkerBody.getLocation() )
		self.walkers[ self.currentWalkerIndex ].setDistanceTraveled( distance )
		print "Walker " , self.currentWalkerIndex , " walked " , distance , " LU in ", self.roundDuration, " TU"
		
		if ( self.currentWalkerIndex == POPULATION_SIZE - 1):
			self.breedWalkers()
			self.startNewTournament()
		else:
			self.startNewRound()

	def breedWalkers( self ):
		print "breeding walkers..."
		self.walkers = quickSort(self.walkers)

		# Print the results and save the best walker to file.
		self.saveWalkerToFile(self.walkers[0])
		print "Results: "
		for w in self.walkers:
			print w.getID() , ": " , w.getDistance()

		# The walkers of the next generation. 
		# The best walkers get to live on in the next generation.
		nextGeneration = self.walkers[:ELITE_COUNT]

		for p in range(0, POPULATION_SIZE - ELITE_COUNT):
			parents = self.chooseParents()
			child = parents[0].breedWith(parents[1])
			child.mutate()
			nextGeneration = nextGeneration + [child]

		self.walkers = nextGeneration
		self.generation = self.generation + 1

	def chooseParents( self ):
		parents = [self.chooseParent()] + [self.chooseParent()]
		if(parents[0].getID() == parents[1].getID()):
			return self.chooseParents()
		return parents

	def chooseParent( self ):
		candidates = []
		for i in range(0,2):
			r = randint(0, POPULATION_SIZE - 1)
			candidates = candidates + [self.walkers[r]]
		if candidates[0].getDistance() > candidates[1].getDistance():
			return candidates[0]
		return candidates[1]

	def compareDistance( self, a, b ):
		return b.getDistance() - a.getDistance()

	def initWalkers( self ):
		self.walkerBody = WalkerBody()
		self.watch( self.walkerBody )
		self.walkers = breve.createInstances( WalkerController, POPULATION_SIZE )
		self.generation = 0
		print "Starting program..."

	def initWalkerIDs( self ):
		for i in range(0, POPULATION_SIZE):
			self.walkers[i].setID(i)

	def initWorld( self ):
		self.setRandomSeedFromDevRandom()
		self.enableFastPhysics()
		self.setFastPhysicsIterations( 40 )
		self.enableLighting()
		self.enableSmoothDrawing()
		self.moveLight( breve.vector( 0, 20, 0 ) )
		floor = breve.Floor()
		floor.catchShadows()
		self.cloudTexture = breve.Image().load( 'images/clouds.png' )
		self.enableShadowVolumes()
		self.enableReflections()
		self.setBackgroundColor( breve.vector( 0.4, 0.6, 0.9 ) )
		self.setBackgroundTextureImage( self.cloudTexture )

		self.offsetCamera( breve.vector( 3, 13, -13 ) )

	def iterate( self ):
		self.walkers[ self.currentWalkerIndex ].applyJointVelocities( self.walkerBody, self.getTime() )
		breve.PhysicalControl.iterate( self )
	
	def saveWalkerToFile( self, walker):
		f = open(SAVED_WALKERS, 'a')
		f.write("d: " + str(walker.getDistance()) + " :genome: " + walker.getGenomeString() + "\n")
		f.close()
		
	def showInfo( self ):
		infoString = "Walker #" + str(self.currentWalkerIndex)
		infoString = infoString + '\n' + " Generation #" + str(self.generation)
		self.setDisplayText( infoString , -0.95, -0.9 )

	# Checks if the walker has not moved since the last status check.
	def walkerIsStill( self ):
		return breve.length( self.walkerBody.getLocation() - self.walkerPrevLocation ) < MOVEMENT_THRESHOLD


def quickSort(list):
    if list == []: 
        return []
    else:
        pivot = list[0]
        lesser = quickSort([x for x in list[1:] if x.getDistance() < pivot.getDistance()])
        greater = quickSort([x for x in list[1:] if x.getDistance() >= pivot.getDistance()])
        return greater + [pivot] + lesser