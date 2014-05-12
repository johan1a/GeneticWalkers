import breve
from QuadrupedGenome import QuadrupedGenome
from WalkerController import WalkerController
from QuadrupedBody import QuadrupedBody

class QuadrupedController( WalkerController ):
	def __init__( self, chromosomes = None):
		super(QuadrupedController, self).__init__(chromosomes)
		self.walkerBody = QuadrupedBody( chromosomes )
		
	def initBody( self ):
		self.walkerBody.initBody( self.getChromosomes() )

	def initGenome( self, chromosomes ):
		self.genome = QuadrupedGenome( chromosomes )