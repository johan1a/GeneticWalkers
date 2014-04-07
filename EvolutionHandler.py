import breve
from WalkerBody import WalkerBody
from WalkerController import WalkerController
from Genome import Genome
from random import randint
import sys
print sys.version
breve.Genome = Genome #takes care of problems with import conflicts in other files 

ROUND_DURATION = 20
POPULATION_SIZE = 30# 30
PARENT_COUNT = 0.2 * POPULATION_SIZE
ELITE_COUNT = 5
CHILDREN_PER_TWO_PARENTS = (POPULATION_SIZE - PARENT_COUNT) // (PARENT_COUNT / 2 )

class EvolutionHandler( breve.PhysicalControl ):
	def __init__( self ):
		breve.PhysicalControl.__init__( self )
		self.initWorld()
		self.initWalkers()
		
	def initWalkers( self ):
		self.walkerBody = WalkerBody()
		self.walkers = breve.objectList()
		self.watch( self.walkerBody )
		self.walkers = breve.createInstances( WalkerController, POPULATION_SIZE )

		ID = 0
		for walker in self.walkers:
			walker.setID( ID )
			ID = ID + 1
		self.currentWalkerIndex = 0
		self.generation = 0

		self.walkerBody.setColors(self.walkers[ self.currentWalkerIndex ].getColors())

		self.schedule( 'switchWalker', ( self.getTime() + ROUND_DURATION) )
		self.showInfo()
		print "Starting program..."

	def switchWalker( self ):
		distance = breve.length( self.walkerBody.getLocation() )
		self.walkers[ self.currentWalkerIndex ].setDistanceTraveled( distance )
		self.walkerBody.center()

		print "Walker " , self.currentWalkerIndex , " walked " , distance , " LU"

		self.currentWalkerIndex = self.currentWalkerIndex + 1 
		if ( self.currentWalkerIndex == POPULATION_SIZE ):
			self.breedWalkers()
			self.currentWalkerIndex = 0

		self.walkerBody.setColors(self.walkers[ self.currentWalkerIndex ].getColors())
		
		self.schedule( 'switchWalker', ( self.getTime() + ROUND_DURATION ) )
		self.showInfo()

	def breedWalkers( self ):
		print '''breeding walkers...'''
		usedWalkers = [] # indices of all used for breeding
		
		sortedWalkers = walkers
		sortedWalkers = quickSort(sortedWalkers)
		for w in sortedWalkers:
			print w.getID() , ": " , w.getDistance()

		childIndex = POPULATION_SIZE - 1 # index of the worst walker in sortedWalkers

		for p in range(0, POPULATION_SIZE - ELITE_COUNT):
			parents = self.chooseParents(usedWalkers, sortedWalkers)
			print "parents: ", parents[0].getID(), ", ", parents[1].getID()

			parents[0].breed(parents[1], sortedWalkers[childIndex])
			sortedWalkers[childIndex].mutate()
			usedWalkers = usedWalkers + [childIndex]
			childIndex = childIndex - 1
			while(childIndex in usedWalkers):
				childIndex = childIndex - 1
			if childIndex == ELITE_COUNT - 1:
				break
		self.generation = self.generation + 1
		
	def chooseParents( self, usedWalkers, sortedWalkers):
		parents = []
		for i in range(0,2):
			parents = parents + [self.chooseParent(usedWalkers, sortedWalkers)]
		print "parents: ", parents[0].getID(), ", ", parents[1].getID()
		return parents

	def chooseParent( self, usedWalkers, sortedWalkers):
		candidates = []
		for i in range(0,2):
			r = randint(0, POPULATION_SIZE - 1)
			#while r in usedWalkers:
			#	r = randint(0, POPULATION_SIZE - 1)
			candidates = candidates + [sortedWalkers[r]]
		print "candidates: ", candidates[0].getID(), ", " , candidates[1].getID()
		if candidates[0].getDistance() >= candidates[1].getDistance():
			indexOfBest = 0
		else:
			indexOfBest = 1
		#usedWalkers = usedWalkers + [indexOfBest] #återläggning??
		return candidates[indexOfBest]

	def compareDistance( self, a, b ):
		return b.getDistance() - a.getDistance()

	def showInfo( self ):
		infoString = "Walker #" + str(self.currentWalkerIndex)
		infoString = infoString + '\n' + " Generation #" + str(self.generation)
		self.setDisplayText( infoString , -0.95, -0.9 )

	def initWorld( self ):
		self.setRandomSeedFromDevRandom()
		#self.enableFastPhysics()
		#self.setFastPhysicsIterations( 5 )
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

def quickSort(list):
    if list == []: 
        return []
    else:
        pivot = list[0]
        lesser = quickSort([x for x in list[1:] if x.getDistance() < pivot.getDistance()])
        greater = quickSort([x for x in list[1:] if x.getDistance() >= pivot.getDistance()])
        return greater + [pivot] + lesser

EvolutionHandler()