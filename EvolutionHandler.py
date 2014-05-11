import breve
from random import randint

#Default configuration values:
configValues = {}
configValues["STOP_ON_MAX_DURATION"] = True
configValues["STOP_ON_FALL"] = False
configValues["ROUND_MAX_DURATION"] = 60
configValues["STATUS_CHECK_INTERVAL"] = 10
configValues["POPULATION_SIZE"] = 30
configValues["ELITE_COUNT"] = 6
configValues["SAVE_FILE"] = "saveFileDefault.txt"

# A walker is considered stationary if it has not moved 
# further than MOVEMENT_THRESHOLD since the last status check.
configValues["MOVEMENT_THRESHOLD"] = 1




class EvolutionHandler( breve.PhysicalControl ):
	def __init__( self, walkerType, configValues = None, scoreFunc = lambda dist, time, uprightRatio: dist ):
		breve.PhysicalControl.__init__( self )
		self.initConfigValues( configValues )
		self.getScore = scoreFunc
		self.walkerType = walkerType
		self.currentWalker = None
		self.initWorld()
		self.initWalkers()
		self.startNewTournament()

	def startNewTournament( self ):
		print "Starting tournament with generation #", self.generation
		self.currentWalkerIndex = -1
		self.initWalkerIDs()
		self.startNewRound()

	def startNewRound( self ):
		self.roundDuration = 0
		self.uprightCount = 0.0

		self.currentWalkerIndex = self.currentWalkerIndex + 1
		self.currentWalker = self.walkers[ self.currentWalkerIndex ]
		self.currentWalker.setupBody()
		
		self.watch( self.currentWalker.getBody() )
 		self.walkerPrevLocation = self.currentWalker.getLocation()

		self.showInfo()
		self.schedule( 'checkWalkerStatus', ( self.getTime() + self.statusCheckInterval ) )

	# Checks if the walker has run out of time or stopped.
	# Switches to the next walker if that is the case.
	def checkWalkerStatus( self ):
		self.roundDuration = self.roundDuration + self.statusCheckInterval
		if( self.currentWalker.isUpright() ):
			self.uprightCount = self.uprightCount + 1

		if( self.roundIsOver() ): 
			self.switchWalker()
		else:
			self.schedule( 'checkWalkerStatus', ( self.getTime() + self.statusCheckInterval ) )
			self.walkerPrevLocation = self.currentWalker.getLocation()

	def roundIsOver( self ):
		return (self.walkerIsStill() or 
			self.stopOnMaxDuration and (self.roundDuration == self.roundMaxDuration) or 
			self.stopOnFall and (not self.currentWalker.isUpright()))

	def switchWalker( self ):
		distance = breve.length( self.currentWalker.getLocation() )
		uprightPercentage = self.uprightCount * self.statusCheckInterval / self.roundDuration 
		score = self.getScore( distance, self.roundDuration, uprightPercentage)

		self.currentWalker.setDistanceTraveled( distance )
		self.currentWalker.setUprightRatio( uprightPercentage )
		self.currentWalker.setScore( score )
		self.currentWalker.deleteBody()

		#print "Walker " , self.currentWalkerIndex , " Score: ", score , " Distance: ", distance, " LU in ", self.roundDuration, " TU. Upright Ratio: ", uprightRatio, "\n"
		print "Walker " , self.currentWalkerIndex , " Score: ", score , " Upright percentage: ", uprightPercentage

		if ( self.currentWalkerIndex == self.populationSize - 1):
			self.breedWalkers()
			self.startNewTournament()
		else:
			self.startNewRound()

	def breedWalkers( self ):
		self.walkers = sortByScore( self.walkers )

		# Print the results and save the two best walkers to file.
		self.saveWalkerToFile(self.walkers[0])
		self.saveWalkerToFile(self.walkers[1])
		print "Results of top 10: "
		print "(ID: Score, Distance, Time)"
		for i in range(0,10):
			print self.walkers[i].getID() , ": " , self.walkers[i].getScore(), ", ", self.walkers[i].getDistance(), ", ", self.walkers[i].getScore()

		# The walkers of the next generation. 
		# The best walkers get to live on in the next generation.
		nextGeneration = self.walkers[:self.eliteCount]

		print "breeding walkers..."
		for p in range(0, self.populationSize - self.eliteCount):
			parents = self.chooseParents()
			childrenGenomes = parents[0].breedWith( parents[1] )
			children = [ self.makeWalkerController( childrenGenomes[i] ) for i in range( 0, len( childrenGenomes ))]
			[ child.mutate() for child in children ]
			nextGeneration = nextGeneration + [child]

		del self.walkers[self.eliteCount:] # Delete unused walker objects

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
			r = randint(0, self.populationSize - 1)
			candidates = candidates + [self.walkers[r]]
		if candidates[0].getDistance() > candidates[1].getDistance():
			return candidates[0]
		return candidates[1]

	def compareDistance( self, a, b ):
		return b.getDistance() - a.getDistance()

	def initWalkers( self ):
		self.walkers = [ self.makeWalkerController() for i in range(0, self.populationSize)] 
		self.generation = 0
		print "Starting program..."

	def initWalkerIDs( self ):
		for i in range(0, len(self.walkers)):
			self.walkers[i].setID(i)

	def initWorld( self ):
		self.setRandomSeedFromDevRandom()
		self.enableFastPhysics()
		self.setFastPhysicsIterations( 40 )
		self.enableLighting()
		self.enableSmoothDrawing()
		self.moveLight( breve.vector( 5, 20, 0 ) )
		floor = breve.Floor()
		floor.catchShadows()
		self.cloudTexture = breve.Image().load( 'images/clouds.png' )
		self.enableShadowVolumes()
		self.enableReflections()
		self.setBackgroundColor( breve.vector( 0.3, 0.6, 0.9 ) )
		self.setBackgroundTextureImage( self.cloudTexture )

		self.offsetCamera( breve.vector( 4, 16, -12 ) )

	def iterate( self ):
		self.currentWalker.applyJointVelocities( self.getTime() )
		breve.PhysicalControl.iterate( self )

	def saveWalkerToFile( self, walker):
		f = open(self.saveFile, 'a')
		f.write(str(walker.getScore()) + ":" + walker.getGenomeString() + "\n")
		f.close()

	def showInfo( self ):
		infoString = "Walker #" + str(self.currentWalkerIndex)
		infoString = infoString + '\n' + " Generation #" + str(self.generation)
		self.setDisplayText( infoString , -0.95, -0.9 )

	# Checks if the walker has not moved since the last status check.
	def walkerIsStill( self ):
		return breve.length( self.currentWalker.getLocation() - self.walkerPrevLocation ) < self.movementThreshold

	# Sets the configuration values
	def initConfigValues( self, customValues = None ):


		if(customValues is not None):
			for key in customValues:
				configValues[key] = customValues[key]

		self.stopOnMaxDuration = configValues["STOP_ON_MAX_DURATION"]
		self.stopOnFall = configValues["STOP_ON_FALL"]
		self.roundMaxDuration = configValues["ROUND_MAX_DURATION"]
		self.statusCheckInterval = configValues["STATUS_CHECK_INTERVAL"]
		self.populationSize = configValues["POPULATION_SIZE"]
		self.eliteCount = configValues["ELITE_COUNT"]
		self.saveFile = configValues["SAVE_FILE"]
		self.movementThreshold = configValues["MOVEMENT_THRESHOLD"]

	def makeWalkerController( self, chromosomes = None ):
		return self.walkerType( chromosomes )


def sortByScore(list):
    if list == []: 
        return []
    else:
        pivot = list[0]
        lesser = sortByScore([x for x in list[1:] if x.getScore() < pivot.getScore()])
        greater = sortByScore([x for x in list[1:] if x.getScore() >= pivot.getScore()])
        return greater + [pivot] + lesser