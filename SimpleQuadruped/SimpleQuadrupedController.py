import breve
from SimpleQuadrupedGenome import SimpleQuadrupedGenome
from WalkerController import WalkerController
from SimpleQuadrupedBody import SimpleQuadrupedBody

class SimpleQuadrupedController( WalkerController ):
	def __init__( self, chromosomes = None):
		super(SimpleQuadrupedController, self).__init__(chromosomes)
		self.walkerBody = SimpleQuadrupedBody( chromosomes )
		
	def initBody( self ):
		self.walkerBody.initBody( self.getChromosomes() )

	def initGenome( self, chromosomes ):
		self.genome = SimpleQuadrupedGenome( chromosomes )