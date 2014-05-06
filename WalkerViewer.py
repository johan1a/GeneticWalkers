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
-1.51185166875 -2.87433195694 -2.99962846887 2.70933577286 -2.05888261315 -2.08271840079 -0.178918643081 2.50860779504 -1.94949001665 -1.110880551 2.18705060161 -0.957504903794 9.60974519474 4.024822617 5.02630593339 1.6715093183 0.725845139341 1.31921752587
"""
g = """
2.65060053141 -2.23285511902 -2.53648988404 -1.90759639998 -0.874799855211 -1.69174624462 0.833407542164 3.00361284291 -2.32348209346 -0.719826019755 -2.35516535499 0.190185739796 8.63687984661 9.09092579452 5.13331671308 0.713860724841 0.742401712431 0.810149378468
"""
#helt ok
g = """
-0.732849900586 -2.32263343833 -2.42601676261 -1.9845324073 2.47030739472 1.24091755816 1.07068138578 0.480444110046 -1.86352097059 0.763552648788 1.82364089218 -1.46774854505 6.61939066582 8.82168103277 5.11863626654 1.36930531879 0.522881420852 1.09223241929
"""g = """
0.320817857973 1.13053157358 -0.753582051757 -1.07382465994 -0.154629477792 -1.22346341487 -1.02572284904 -2.75484015749 0.345623342 3.01064128964 -0.518568254984 1.68892638009 5.10218264207 8.28913219656 5.25774897991 0.648779381994 1.26465041823 1.29451738256
"""

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
		self.walker.applyJointVelocities( self.walkerBody, self.getTime() )
		breve.PhysicalControl.iterate( self )
	
WalkerViewer()