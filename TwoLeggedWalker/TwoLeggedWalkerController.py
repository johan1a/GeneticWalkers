import breve
from TwoLeggedWalkerGenome import TwoLeggedWalkerGenome
from WalkerController import WalkerController
from TwoLeggedWalkerBody import TwoLeggedWalkerBody

class TwoLeggedWalkerController( WalkerController ):
	def __init__( self, chromosomes = None):
		super(TwoLeggedWalkerController, self).__init__(chromosomes)
		self.walkerBody = TwoLeggedWalkerBody( chromosomes )
		
	def initBody( self ):
		self.walkerBody.initBody( self.getChromosomes() )

	def initGenome( self, chromosomes ):
		self.genome = TwoLeggedWalkerGenome( chromosomes )
