import breve
from EightLeggedWalkerGenome import EightLeggedWalkerGenome
from WalkerController import WalkerController
from EightLeggedWalkerBody import EightLeggedWalkerBody

class EightLeggedWalkerController( WalkerController ):
	def __init__( self, chromosomes = None):
		super(EightLeggedWalkerController, self).__init__(chromosomes)
		self.walkerBody = EightLeggedWalkerBody( chromosomes )
		
	def initBody( self ):
		self.walkerBody.initBody( self.getChromosomes() )

	def initGenome( self, chromosomes ):
		self.genome = EightLeggedWalkerGenome( chromosomes )