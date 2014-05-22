import breve

srcDir = sys.path[-1]
sys.path.append(srcDir + '\\Quadruped')
sys.path.append(srcDir + '\\Common')
from QuadrupedController import QuadrupedController
from EvolutionHandler import EvolutionHandler

configValues = {}
configValues["ROUND_MAX_DURATION"] = 60
configValues["STATUS_CHECK_INTERVAL"] = 5
configValues["POPULATION_SIZE"] = 40
configValues["ELITE_COUNT"] = 6
configValues["BEST_WALKERS_SAVE_FILE"] = "quadrupeds.txt"
configValues["AUTOSAVE_ACTIVE"] = True
configValues["SIMULATION_SAVE_FILE"] = "quadruped_simulation_save.txt"
configValues["START_FROM_STORED_PROGRESS"] = False
configValues["AUTOSAVE_INTERVAL"] = 10

def scoreFunc( dist, time, uprightPercentage ):
	#return dist * ( 0.5 + 0.5 * uprightPercentage ) + dist / time
	return dist

EvolutionHandler( QuadrupedController, configValues, scoreFunc )