import breve
from BipedGenome import BipedGenome
from WalkerController import WalkerController
from BipedBody import BipedBody

class BipedController( WalkerController ):
	def __init__( self, chromosomes = None):
		super(BipedController, self).__init__(chromosomes)
		self.walkerBody = BipedBody( chromosomes )
		
	def initBody( self ):
		self.walkerBody.initBody( self.getChromosomes() )

	def initGenome( self, chromosomes ):
		self.genome = BipedGenome( chromosomes )
