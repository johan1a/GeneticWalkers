import breve

srcDir = sys.path[-1]
sys.path.append(srcDir + '\\SimpleQuadruped')
sys.path.append(srcDir + '\\Common')
from SimpleQuadrupedController import SimpleQuadrupedController
from EvolutionHandler import EvolutionHandler

configValues = {}
configValues["ROUND_MAX_DURATION"] = 60
configValues["STATUS_CHECK_INTERVAL"] = 5
configValues["POPULATION_SIZE"] = 50
configValues["ELITE_COUNT"] = 6
configValues["BEST_WALKERS_SAVE_FILE"] = "simple_quadrupeds.txt"
configValues["AUTOSAVE_ACTIVE"] = True
configValues["SIMULATION_SAVE_FILE"] = "SQ_simulation_save.txt"
configValues["START_FROM_STORED_PROGRESS"] = True
configValues["AUTOSAVE_INTERVAL"] = 10

def scoreFunc( dist, time, uprightPercentage ):
	return dist * ( 0.5 + 0.5 * uprightPercentage )

EvolutionHandler( SimpleQuadrupedController, configValues, scoreFunc )