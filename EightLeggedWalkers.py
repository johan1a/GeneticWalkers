import breve
from EvolutionHandler import EvolutionHandler
sys.path.append('E:\\Dropbox\\Skola\\EDAN50\\GeneticWalkers\\EightLeggedWalker')
from EightLeggedWalkerController import EightLeggedWalkerController

configValues = {}
configValues["ROUND_MAX_DURATION"] = 60
configValues["STATUS_CHECK_INTERVAL"] = 10
configValues["POPULATION_SIZE"] = 30
configValues["ELITE_COUNT"] = 6
configValues["SAVE_FILE"] = "EightLeggedWalkers.txt"

def scoreFunc( dist, time, uprightPercentage ):
	return dist*(0.5 + 0.5 * uprightPercentage)

EvolutionHandler( EightLeggedWalkerController, configValues, scoreFunc )