import breve
import sys
print sys.version
from WalkerBody import WalkerBody
from WalkerController import WalkerController
from Genome import Genome
from random import randint
breve.Genome = Genome # takes care of problems with import conflicts in other files 
#genome = [1.28358265241, 2.27558417881, -1.80042392019, -0.107369341751, -1.51048552499, 0.677948039621, -3.06073744831, 2.08250112473, 2.83727253916, 3.68920889123]
g = "1.28358265241 2.27558417881 -1.99161113192 -0.514256660802 -1.51048552499 0.677948039621 -3.06073744831 2.3904053083 2.83727253916 3.68920889123"
g = "1.28358265241 2.27558417881 -1.80042392019 -0.514256660802 -1.51048552499 0.677948039621 -3.06073744831 2.3904053083 2.74338466348 3.62708183166"
genome = map(float, g.split(' '))

class WalkerViewer( breve.PhysicalControl ):
	def __init__( self ):
		breve.PhysicalControl.__init__( self )
		self.initWorld()
		self.initWalker()

	def initWalker( self ):
		self.walkerBody = WalkerBody()
		self.walkerBody.center()
		self.watch( self.walkerBody )
		self.walker = WalkerController()
		self.walker.setGenome( genome )
		print "Starting program..."

	def initWorld( self ):
		self.setRandomSeedFromDevRandom()
		self.enableFastPhysics()
		self.setFastPhysicsIterations( 40 )
		self.enableLighting()
		self.enableSmoothDrawing()
		self.moveLight( breve.vector( 0, 20, 0 ) )
		floor = breve.Floor()
		floor.catchShadows()
		self.cloudTexture = breve.Image().load( 'images/clouds.png' )
		self.enableShadowVolumes()
		self.enableReflections()
		self.setBackgroundColor( breve.vector( 0.4, 0.6, 0.9 ) )
		self.setBackgroundTextureImage( self.cloudTexture )

		self.offsetCamera( breve.vector( 3, 13, -13 ) )

	def iterate( self ):
		self.walker.applyJointVelocities( self.walkerBody, self.getTime() )
		breve.PhysicalControl.iterate( self )
	
WalkerViewer()