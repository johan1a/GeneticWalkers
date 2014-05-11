import breve
import sys
print sys.version
sys.path.append('E:\\Dropbox\\Skola\\EDAN50\\GeneticWalkers\\TwoLeggedWalker')
sys.path.append('E:\\Dropbox\\Skola\\EDAN50\\GeneticWalkers\\FourLeggedWalker')
sys.path.append('E:\\Dropbox\\Skola\\EDAN50\\GeneticWalkers\\EightLeggedWalker')
from TwoLeggedWalkerController import TwoLeggedWalkerController
from FourLeggedWalkerController import FourLeggedWalkerController
from EightLeggedWalkerController import EightLeggedWalkerController
from random import randint



#helt ok
input = """
ignore:FourLegged:-0.732849900586 -2.32263343833 -2.42601676261 -1.9845324073 2.47030739472 1.24091755816 1.07068138578 0.480444110046 -1.86352097059 0.763552648788 1.82364089218 -1.46774854505 6.61939066582 8.82168103277 5.11863626654 1.36930531879 0.522881420852 1.09223241929
"""
input = """
158.393055019:FourLegged:0.384476296416 -1.51447220492 0.555783633514 -0.117190716847 -1.16754187945 -2.72350984167 2.8642172252 -3.10076078271 -2.56620256967 -2.45667834197 0.907396333928 -0.425301149532 -13.3745907548 7.10721917661 5.88767465332 0.511923271662 1.1049933617 1.34263943348
"""
#moonwalk
input = """
178.025263215:FourLegged:0.403407968072 -1.51447220492 0.608573745375 -0.112476445778 -1.28290645325 -2.99352917021 2.90714317147 -3.14580170972 -2.56620256967 -2.45667834197 0.901846426175 -0.425301149532 -13.542109591 8.10051802441 5.88767465332 0.511923271662 1.04092226273 1.25151863285
"""

####################################
#stationary

input = """
16:TwoLegged:-2.01314382959 -1.15962566466 2.4726914515 2.38431969976 5.44600714704 3.54999012826 10.1871019338
"""
input = """
7.67001255429:TwoLegged:0.915718502693 2.99089984803 -2.34322039578 1.88179380046 9.61778607642 0.0 0.0450689506347
"""

##############################################
input = """
161.185697934:EightLegged:-2.70184827105 -2.41714859924 -2.906265298 1.08554373982 -3.15518124579 7.51720476236
"""

input = """
204.974993631:EightLegged:-1.95898075832 -1.31725906545 -0.641425677847 0.702355534735 6.87149261287 3.03972764665
"""

##############################################

input = """
209.552309855:FourLegged:-1.86461619074 1.13727554129 -0.630695626939 -1.83191117588 -2.15591127913 -1.78003933913 -2.98549955657 -2.17518618541 1.23047454203 -0.759986478151 -1.68056708534 -2.08472249672 -9.05835456993 7.86172704212 6.51286745962 1.28292093312 1.75127121782 2.14322206277"""



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
		elif( type == "EightLegged"):
			return EightLeggedWalkerController( chromosomes )

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