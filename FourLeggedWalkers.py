import breve
from EvolutionHandler import EvolutionHandler
sys.path.append('E:\\Dropbox\\Skola\\EDAN50\\GeneticWalkers\\FourLeggedWalker')
from FourLeggedWalkerController import FourLeggedWalkerController

configValues["MAX_DURATION_CHECK"] = True
configValues["ROUND_MAX_DURATION"] = 60
configValues["STATUS_CHECK_INTERVAL"] = 10
configValues["POPULATION_SIZE"] = 60
configValues["ELITE_COUNT"] = 10
configValues["SAVE_FILE"] = "FourLeggedWalkers.txt"
configValues["MOVEMENT_THRESHOLD"] = 1

EvolutionHandler( FourLeggedWalkerController, configValues )