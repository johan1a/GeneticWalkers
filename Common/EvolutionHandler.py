import breve
from random import randint

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

	# Starts a new tournament.
	def startNewTournament( self ):
		print "Starting the tournament of generation #", self.generation
		self.currentWalkerIndex = -1
		for i in range(0, len( self.walkers ) ):
			self.walkers[i].setID(i)
		self.startNewRound()

	# Starts a new round.
	def startNewRound( self ):
		self.roundDuration = 0
		self.uprightCount = 0.0

		self.currentWalkerIndex = self.currentWalkerIndex + 1
		self.currentWalker = self.walkers[ self.currentWalkerIndex ]
		self.currentWalker.setupBody()
		
		self.watch( self.currentWalker.getBody() )
 		self.walkerPrevLocation = self.currentWalker.getLocation()

		self.showInfo()
		self.schedule( 'checkWalkerStatus', ( self.getTime() + configValues["STATUS_CHECK_INTERVAL"] ) )

	# Checks if stopping conditions are met,
	# and switches to the next walker if that is the case.
	def checkWalkerStatus( self ):
		self.roundDuration = self.roundDuration + configValues["STATUS_CHECK_INTERVAL"]
		if( self.currentWalker.isUpright() ):
			self.uprightCount = self.uprightCount + 1

		if( self.roundIsOver() ): 
			self.switchWalker()
		else:
			self.schedule( 'checkWalkerStatus', ( self.getTime() + configValues["STATUS_CHECK_INTERVAL"] ) )
			self.walkerPrevLocation = self.currentWalker.getLocation()

	# Checks if the round is over or not.
	def roundIsOver( self ):
		return ( configValues["STOP_ON_STATIONARY"] and self.walkerIsStill() or 
			configValues["STOP_ON_MAX_DURATION"] and (self.roundDuration == configValues["ROUND_MAX_DURATION"]) or 
			configValues["STOP_ON_FALL"] and not self.currentWalker.isUpright() )

	# Evaluates the performance of the walker and then starts a new round.
	# If the previous walker was the last one, a new generation is bred
	# and a new tournament started.
	def switchWalker( self ):
		distance = breve.length( self.currentWalker.getLocation() )
		uprightPercentage = self.uprightCount * configValues["STATUS_CHECK_INTERVAL"] / self.roundDuration 
		score = self.getScore( distance, self.roundDuration, uprightPercentage)

		self.currentWalker.setDistanceTraveled( distance )
		self.currentWalker.setUprightRatio( uprightPercentage )
		self.currentWalker.setScore( score )
		self.currentWalker.setTime( self.roundDuration )
		self.currentWalker.deleteBody()

		#print "Walker " , self.currentWalkerIndex , ": Score: ", score , ", Distance: ", distance, ", Time: " , self.roundDuration ,", Upright Ratio: ", uprightPercentage
		print "Walker " , self.currentWalkerIndex , ": Score: ", score

		if ( self.currentWalkerIndex == configValues["POPULATION_SIZE"] - 1 ):
			self.breedWalkers()

			if(configValues["AUTOSAVE_ACTIVE"] and self.generation % configValues["AUTOSAVE_INTERVAL"] == 0):
				self.saveGenerationToFile()

			self.startNewTournament()
		else:
			self.startNewRound()


	# Breeds a new generation using tournament selection.
	def breedWalkers( self ):
		self.walkers = sortByScore( self.walkers )

		# Prints the results and saves the best walker to file.
		self.saveWalkerToFile(self.walkers[0])

		if( configValues["POPULATION_SIZE"] >= 10 ):
			print
			print "Results of the top 10 walkers: "
			print "ID: Score, Distance, Time, Upright Ratio\n"
			for i in range(0,10):
				print self.walkers[i].getID() , ": " , self.walkers[i].getScore(), ", ", self.walkers[i].getDistance(), ", ", self.walkers[i].getTime(), ", ", self.walkers[i].getUprightRatio() 
			print
		# The walkers of the next generation. 
		# The best ("elite") walkers get to live on in the next generation.
		nextGeneration = self.walkers[:configValues["ELITE_COUNT"]]

		print "Breeding a new generation...\n"
		for p in range(0, configValues["POPULATION_SIZE"] - configValues["ELITE_COUNT"]):
			parents = self.chooseParents()
			childrenGenomes = parents[0].breedWith( parents[1] )
			children = [ self.makeWalkerController( childrenGenomes[i] ) for i in range( 0, len( childrenGenomes ))]
			[ child.mutate() for child in children ]
			nextGeneration = nextGeneration + [child]

		del self.walkers[configValues["ELITE_COUNT"]:] # Delete unused walker objects

		self.walkers = nextGeneration
		self.generation = self.generation + 1

	# Selects two parents using tournament selection.
	def chooseParents( self ):
		parents = ( self.chooseParent(), self.chooseParent() )
		if(parents[0].getID() == parents[1].getID()):
			return self.chooseParents()
		return parents

	# Picks two random individuals from the current generation
	# and returns the one with the highest fitness score.
	def chooseParent( self ):
		candidates = [ self.walkers[ randint(0, configValues["POPULATION_SIZE"] - 1) ] for i in range( 0, 2 ) ]
		if candidates[0].getDistance() > candidates[1].getDistance():
			return candidates[0]
		return candidates[1]

	# Creates a new walker generation or loads it from file, depening on config settings.
	def initWalkers( self ):
		print
		print "Initializing...\n"
		if(configValues["START_FROM_STORED_PROGRESS"]):
			self.loadGenerationFromFile()
		else:
			self.walkers = [ self.makeWalkerController() for i in range(0, configValues["POPULATION_SIZE"])] 
			self.generation = 0

	# Loads a stored generation and sets it as current generation.
	def loadGenerationFromFile( self ):
		print "Loading saved progress...\n"
		f = open(configValues["SIMULATION_SAVE_FILE"], 'r')
		self.generation = int( f.readline() )
		tempW = f.readlines()
		self.walkers = map( lambda w: self.makeWalkerController( map( float, w.split(':')[1].split(' ') ) ), tempW )
		f.close()
		
	# Saves the entire current generation to file.
	def saveGenerationToFile( self ):
		print "Saving progress...\n"
		f = open(configValues["SIMULATION_SAVE_FILE"], 'w')
		f.write( str( self.generation ) + '\n')
		for walker in self.walkers:
			f.write( walker.getGenomeString() + '\n')
		f.close()

	# Saves the given walker to file.
	def saveWalkerToFile( self, walker):
		f = open(configValues["BEST_WALKERS_SAVE_FILE"], 'a')
		f.write(str(walker.getScore()) + ":" + str(self.generation) + ":" + walker.getGenomeString() + "\n")
		f.close()

	# Initializes the simulation environment.
	def initWorld( self ):
		#self.enableFastPhysics()
		#self.setFastPhysicsIterations( 40 )
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

	# Shows a small info text onscreen.
	def showInfo( self ):
		infoString = "Walker #" + str(self.currentWalkerIndex)
		infoString = infoString + '\n' + " Generation #" + str(self.generation)
		self.setDisplayText( infoString , -0.95, -0.9 )

	# Checks if the walker has not moved since the last status check.
	def walkerIsStill( self ):
		return breve.length( self.currentWalker.getLocation() - self.walkerPrevLocation ) < configValues["MOVEMENT_THRESHOLD"]

	# Sets the configuration values
	def initConfigValues( self, customValues = None ):
		if(customValues):
			for key in customValues:
				configValues[key] = customValues[key]

	# Returns a walker instance.
	def makeWalkerController( self, chromosomes = None ):
		return self.walkerType( chromosomes )

# Quicksort implementation because of old Python version...
def sortByScore(list):
    if list == []: 
        return []
    else:
        pivot = list[0]
        lesser = sortByScore([x for x in list[1:] if x.getScore() < pivot.getScore()])
        greater = sortByScore([x for x in list[1:] if x.getScore() >= pivot.getScore()])
        return greater + [pivot] + lesser


#Default configuration values:
configValues = {}
configValues["STOP_ON_MAX_DURATION"] = True
configValues["STOP_ON_FALL"] = False
configValues["ROUND_MAX_DURATION"] = 60
configValues["STATUS_CHECK_INTERVAL"] = 10
configValues["POPULATION_SIZE"] = 30
configValues["ELITE_COUNT"] = 6

# If true, a round is stopped when the walker is stationary.
configValues["STOP_ON_STATIONARY"] = True

# A walker is considered stationary if it has not moved 
# further than MOVEMENT_THRESHOLD since the last status check.
configValues["MOVEMENT_THRESHOLD"] = 1

# File containing the best walker of every generation.
configValues["BEST_WALKERS_SAVE_FILE"] = "best_walkers_save_default.txt"

# Enables autosaving so the progress can be continued upon another time.
configValues["AUTOSAVE_ACTIVE"] = False

# The file used for saving progress.
configValues["SIMULATION_SAVE_FILE"] = "simulation_save_default.txt"

# Whether or not to start the simulation with the generation stored in SIMULATION_SAVE_FILE.
configValues["START_FROM_STORED_PROGRESS"] = False

# The number of generations between each autosave.
configValues["AUTOSAVE_INTERVAL"] = 10