import breve
import sys
print sys.version
from WalkerBody import WalkerBody
from WalkerController import WalkerController
from Genome import Genome
from random import randint
breve.Genome = Genome # takes care of problems with import conflicts in other files 


g = """
2.65060053141 -2.10128447608 -2.49247468388 -2.2327153296 -0.756676256132 -1.86924781038 0.833407542164 -3.12129684453 -2.32348209346 -0.719826019755 -2.35516535499 0.190185739796 8.63687984661 9.09092579452 5.13331671308 0.713860724841 0.742401712431 0.810149378468"""

g = """
2.65060053141 -2.23285511902 -2.53648988404 -1.90759639998 -0.874799855211 -1.69174624462 0.833407542164 3.00361284291 -2.32348209346 -0.719826019755 -2.35516535499 0.190185739796 8.63687984661 9.09092579452 5.13331671308 0.713860724841 0.742401712431 0.810149378468
"""

g = """
-1.51185166875 -2.87433195694 -2.99962846887 2.70933577286 -2.05888261315 -2.08271840079 -0.178918643081 2.50860779504 -1.94949001665 -1.110880551 2.18705060161 -0.957504903794 9.60974519474 4.024822617 5.02630593339 1.6715093183 0.725845139341 1.31921752587
"""
g = """
1.24431332964 2.97635134774 0.920504181788 -0.653348965716 2.78501683101 2.26523105259 1.67864375183 2.8777090307 2.01169508536 1.79738327588 2.86462707328 1.81039758818 8.5256632798 9.16078879619 6.81944705578 0.761480330349 1.26200111896 1.41216448036"""
genome = map(float, g.split(' '))

class WalkerViewer( breve.PhysicalControl ):
	def __init__( self ):
		breve.PhysicalControl.__init__( self )
		self.initWorld()
		self.initWalker()

	def initWalker( self ):
		self.walkerBody = WalkerBody()
		self.walkerBody.initBody(genome)
		self.walkerBody.setColors([breve.randomExpression( breve.vector( 1, 1, 1 ) ), breve.randomExpression( breve.vector( 1, 1, 1 ) )])
		self.walkerBody.center()
		self.watch( self.walkerBody )

		self.walker = WalkerController(genome)
		
		print "Starting program..."

	def initWorld( self ):
		self.setRandomSeedFromDevRandom()
		#self.enableFastPhysics()
		#self.setFastPhysicsIterations( 40 )
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
		self.walker.applyJointVelocities( self.walkerBody, self.getTime() )
		breve.PhysicalControl.iterate( self )
	
WalkerViewer()