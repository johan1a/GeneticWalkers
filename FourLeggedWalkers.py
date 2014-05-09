import breve
from EvolutionHandler import EvolutionHandler
sys.path.append('E:\\Dropbox\\Skola\\EDAN50\\GeneticWalkers\\FourLeggedWalker')
from FourLeggedWalkerController import FourLeggedWalkerController

configValues = {}
configValues["ROUND_MAX_DURATION"] = 60
configValues["STATUS_CHECK_INTERVAL"] = 5
configValues["POPULATION_SIZE"] = 30
configValues["ELITE_COUNT"] = 6
configValues["SAVE_FILE"] = "FourLeggedWalkers.txt"

def scoreFunc( dist, time, uprightPercentage ):
	return dist*(0.5 + 0.5 * uprightPercentage)

EvolutionHandler( FourLeggedWalkerController, configValues, scoreFunc )