import breve
import sys
print sys.version
from WalkerBody import WalkerBody
from WalkerController import WalkerController
from Genome import Genome
from random import randint
breve.Genome = Genome # takes care of problems with import conflicts in other files 


g = "0.0860385311332 -0.120679504711 -0.924597734509 1.97496378067 -2.50684928228 -1.81097398914 2.72179527687 0.956908322985 -3.13598009506 2.6908170596 -2.18316182757 -0.819708617539 -8.55846926932 6.4879072571 5.41217668914 1.46880346625 1.15705564537 1.48487549897"
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
		print(self.walkerBody.isUpright())
	
WalkerViewer()