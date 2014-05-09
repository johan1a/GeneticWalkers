import breve
from FourLeggedWalkerGenome import FourLeggedWalkerGenome
from WalkerController import WalkerController
from FourLeggedWalkerBody import FourLeggedWalkerBody

class FourLeggedWalkerController( WalkerController ):
	def __init__( self, chromosomes = None):
		super(FourLeggedWalkerController, self).__init__(chromosomes)
		self.walkerBody = FourLeggedWalkerBody( chromosomes )
		
	def initBody( self ):
		self.walkerBody.initBody( self.getChromosomes() )

	def initGenome( self, chromosomes ):
		self.genome = FourLeggedWalkerGenome( chromosomes )