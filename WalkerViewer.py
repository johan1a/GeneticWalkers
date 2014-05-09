import breve
import sys
print sys.version
sys.path.append('E:\\Dropbox\\Skola\\EDAN50\\GeneticWalkers\\TwoLeggedWalker')
sys.path.append('E:\\Dropbox\\Skola\\EDAN50\\GeneticWalkers\\FourLeggedWalker')
from TwoLeggedWalkerController import TwoLeggedWalkerController
from FourLeggedWalkerController import FourLeggedWalkerController

from random import randint



#helt ok
input = """
ignore:FourLegged:-0.732849900586 -2.32263343833 -2.42601676261 -1.9845324073 2.47030739472 1.24091755816 1.07068138578 0.480444110046 -1.86352097059 0.763552648788 1.82364089218 -1.46774854505 6.61939066582 8.82168103277 5.11863626654 1.36930531879 0.522881420852 1.09223241929
"""

#honorable mention
input = """
51.1424976888:TwoLegged:2.46015405967 0.572652673524 1.01248645512 7.09351885169 5.0522070833 0 2.06357210153
"""
input = """
7.67001255429:TwoLegged:0.915718502693 2.99089984803 -2.34322039578 1.88179380046 9.61778607642 0.0 0.0450689506347
"""



walkerType = input.split(':')[1]
chromosomes = map(float, input.split(':')[2].split(' '))

class WalkerViewer( breve.PhysicalControl ):
	def __init__( self ):
		breve.PhysicalControl.__init__( self )
		self.initWorld()
		self.initWalker()

	def initWalker( self ):
		self.walker = self.makeWalker( walkerType, chromosomes )
		self.walker.setupBody()
		self.watch( self.walker.getBody() )
		
		print "Starting program..."

	def makeWalker( self, type, chromosomes):
		if( type == "FourLegged"):
			return FourLeggedWalkerController( chromosomes )
		elif( type == "TwoLegged"):
			return TwoLeggedWalkerController( chromosomes )

	def initWorld( self ):
		self.setRandomSeedFromDevRandom()
		self.enableFastPhysics()
		self.setFastPhysicsIterations( 40 )
		self.enableLighting()
		self.enableSmoothDrawing()
		self.moveLight( breve.vector( 10, 20, 0 ) )
		floor = breve.Floor()
		floor.catchShadows()
		self.cloudTexture = breve.Image().load( 'images/clouds.png' )
		self.enableShadowVolumes()
		#self.enableReflections()
		self.setBackgroundColor( breve.vector( 0.4, 0.6, 0.9 ) )
		self.setBackgroundTextureImage( self.cloudTexture )

		self.offsetCamera( breve.vector( 3, 13, -13 ) )

	def iterate( self ):
		self.walker.applyJointVelocities( self.getTime() )
		breve.PhysicalControl.iterate( self )
	
WalkerViewer()