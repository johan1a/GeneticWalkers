import breve

srcDir = sys.path[-1]
sys.path.append(srcDir + '\\Octoped')
sys.path.append(srcDir + '\\Common')
from EvolutionHandler import EvolutionHandler
from OctopedController import OctopedController

configValues = {}
configValues["ROUND_MAX_DURATION"] = 60
configValues["STATUS_CHECK_INTERVAL"] = 10
configValues["POPULATION_SIZE"] = 30
configValues["ELITE_COUNT"] = 6
configValues["BEST_WALKERS_SAVE_FILE"] = "octopeds.txt"
configValues["AUTOSAVE_ACTIVE"] = True
configValues["SIMULATION_SAVE_FILE"] = "octoped_simulation_save.txt"
configValues["START_FROM_STORED_PROGRESS"] = False
configValues["AUTOSAVE_INTERVAL"] = 10


def scoreFunc( dist, time, uprightPercentage ):
	return dist

EvolutionHandler( OctopedController, configValues, scoreFunc )