import breve
from EvolutionHandler import EvolutionHandler
sys.path.append('E:\\Dropbox\\Skola\\EDAN50\\GeneticWalkers\\TwoLeggedWalker')
from TwoLeggedWalkerController import TwoLeggedWalkerController

configValues = {}
configValues["STOP_ON_MAX_DURATION"] = False
configValues["STOP_ON_FALL"] = True
configValues["STATUS_CHECK_INTERVAL"] = 1
configValues["POPULATION_SIZE"] = 30
configValues["ELITE_COUNT"] = 6
configValues["SAVE_FILE"] = "TwoLeggedWalkers.txt"
configValues["MOVEMENT_THRESHOLD"] = 0.001

def scoreFunc( dist, time, uprightPercentage ):
	return time

EvolutionHandler( TwoLeggedWalkerController, configValues, scoreFunc )