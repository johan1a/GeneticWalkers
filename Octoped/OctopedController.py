import breve
from OctopedGenome import OctopedGenome
from WalkerController import WalkerController
from OctopedBody import OctopedBody

class OctopedController( WalkerController ):
	def __init__( self, chromosomes = None):
		super(OctopedController, self).__init__(chromosomes)
		self.walkerBody = OctopedBody( chromosomes )
		
	def initBody( self ):
		self.walkerBody.initBody( self.getChromosomes() )

	def initGenome( self, chromosomes ):
		self.genome = OctopedGenome( chromosomes )