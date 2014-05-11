import breve
from EvolutionHandler import EvolutionHandler
sys.path.append('E:\\Dropbox\\Skola\\EDAN50\\GeneticWalkers\\EightLeggedWalker')
from EightLeggedWalkerController import EightLeggedWalkerController

configValues = {}
configValues["ROUND_MAX_DURATION"] = 60
configValues["STATUS_CHECK_INTERVAL"] = 10
configValues["POPULATION_SIZE"] = 30
configValues["ELITE_COUNT"] = 6
configValues["SAVE_FILE"] = "eight_legged_walkers.txt"
configValues["AUTOSAVE_ACTIVE"] = True
configValues["SIMULATION_SAVE_FILE"] = "ELW_simulation_save_test.txt"
configValues["START_FROM_STORED_PROGRESS"] = True
configValues["AUTOSAVE_INTERVAL"] = 50


def scoreFunc( dist, time, uprightPercentage ):
	return dist * (0.5 + 0.5 * uprightPercentage)

EvolutionHandler( EightLeggedWalkerController, configValues, scoreFunc )