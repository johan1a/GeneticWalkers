import breve

srcDir = sys.path[-1]
sys.path.append(srcDir + '\\Biped')
sys.path.append(srcDir + '\\Common')
from BipedController import BipedController
from EvolutionHandler import EvolutionHandler

configValues = {}
configValues["STOP_ON_MAX_DURATION"] = False
configValues["STOP_ON_FALL"] = True
configValues["STOP_ON_STATIONARY"] = False
configValues["STATUS_CHECK_INTERVAL"] = 1
configValues["POPULATION_SIZE"] = 60
configValues["ELITE_COUNT"] = 6
configValues["BEST_WALKERS_SAVE_FILE"] = "bipeds.txt"
configValues["AUTOSAVE_ACTIVE"] = True
configValues["SIMULATION_SAVE_FILE"] = "biped_simulation_save.txt"
configValues["START_FROM_STORED_PROGRESS"] = True
configValues["AUTOSAVE_INTERVAL"] = 10

def scoreFunc( dist, time, uprightPercentage ):
	return time

EvolutionHandler( BipedController, configValues, scoreFunc )