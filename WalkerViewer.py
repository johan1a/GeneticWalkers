import breve, os

srcDir = sys.path[-2]
sys.path.append(srcDir + '\\Common')
sys.path.append(srcDir + '\\Biped')
sys.path.append(srcDir + '\\Quadruped')
sys.path.append(srcDir + '\\SimpleQuadruped')
sys.path.append(srcDir + '\\Octoped')

from BipedController import BipedController
from QuadrupedController import QuadrupedController
from OctopedController import OctopedController
from SimpleQuadrupedController import SimpleQuadrupedController
from random import randint


####################################
#Biped stationary

input = """
16:Biped:ignore:-2.01314382959 -1.15962566466 2.4726914515 2.38431969976 5.44600714704 3.54999012826 10.1871019338
"""

input = """
7.67001255429:ignore:Biped:0.915718502693 2.99089984803 -2.34322039578 1.88179380046 9.61778607642 0.0 0.0450689506347
"""


input = """
200:3:Biped:-2.14950045488 -0.0108564202846 1.06729937097 0.131015756893 0.12042087553 0.041420715205 -0.345440548044

"""
input = """

622:11:Biped:1.14484959043 -2.59588729492 -2.53498739821 0.0310261336371 0.0786342219362 0.041420715205 -0.608213388891

"""
input = """
1074:20:Biped:1.14484959043 -2.59588729492 -2.53498739821 0.0310261336371 0.0786342219362 0.041420715205 -0.608213388891
"""

input ="""
1653:30:Biped:1.11384645181 -1.27723179102 -2.53498739821 0.0310261336371 0.0786342219362 0.041420715205 -0.608213388891
"""

####################################
#Quadruped 
input = """
ignore:ignore:Quadruped:-0.732849900586 -2.32263343833 -2.42601676261 -1.9845324073 2.47030739472 1.24091755816 1.07068138578 0.480444110046 -1.86352097059 0.763552648788 1.82364089218 -1.46774854505 6.61939066582 8.82168103277 5.11863626654 1.36930531879 0.522881420852 1.09223241929
"""

input = """
158.393055019:ignore:Quadruped:0.384476296416 -1.51447220492 0.555783633514 -0.117190716847 -1.16754187945 -2.72350984167 2.8642172252 -3.10076078271 -2.56620256967 -2.45667834197 0.907396333928 -0.425301149532 -13.3745907548 7.10721917661 5.88767465332 0.511923271662 1.1049933617 1.34263943348
"""

input = """
178.025263215:ignore:Quadruped:0.403407968072 -1.51447220492 0.608573745375 -0.112476445778 -1.28290645325 -2.99352917021 2.90714317147 -3.14580170972 -2.56620256967 -2.45667834197 0.901846426175 -0.425301149532 -13.542109591 8.10051802441 5.88767465332 0.511923271662 1.04092226273 1.25151863285
"""


input ="""

225.327211357:12:Quadruped:-0.17351804227 2.75188506578 1.86570192454 -0.527035641581 -0.756349111348 -0.386135330612 2.00410042423 -0.797624832946 2.37376802391 0.788231073802 2.57494520369 0.700706681098 18.2864925441 6.85344888052 5.22927005039 0.855203419529 0.774854218396 1.04656334942
"""

##############################################

input = """
161.185697934:ignore:Octoped:-2.70184827105 -2.41714859924 -2.906265298 1.08554373982 -3.15518124579 7.51720476236
"""

input = """
204.974993631:Octoped:-1.95898075832 -1.31725906545 -0.641425677847 0.702355534735 6.87149261287 3.03972764665
"""

input ="""
258.673475109:21:Octoped:0.626948772466 0.678760738497 1.21919788847 2.70423590488 8.88287692263 4.83967667001
"""

input ="""
301.056728922:38:Octoped:0.577368704905 0.678760738497 1.16567150732 3.25498915392 8.24695521458 4.64279951867
"""

input ="""
295.192748681:104:Octoped:0.720140042915 0.629423001422 1.25593796168 3.0847079473 7.80452210618 4.58128901335
"""


##############################################

input ="""

164.333994512:48:Quadruped:0.791003684358 -2.14365503654 0.827252641487 0.909212535531 -2.25345750056 0.659064703892 1.72488708333 2.66147565512 -2.82239926013 -2.73242490304 0.718920301682 -1.4310296031 11.5966397243 5.75279743237 3.31474329961 0.930098484191 0.711870189619 1.26634494868



"""

input ="""
146.155210914:30:SimpleQuadruped:1.00211352327 -0.954733793089 1.75492364897 1.42856492624 -0.716719211628 -1.91239659154 -0.270137184375 -0.681517292315 22.2087671617 6.14928831116


"""
input ="""
295.192748681:104:Octoped:0.720140042915 0.629423001422 1.25593796168 3.0847079473 7.80452210618 4.58128901335
"""
input ="""
1653:30:Biped:1.11384645181 -1.27723179102 -2.53498739821 0.0310261336371 0.0786342219362 0.041420715205 -0.608213388891
"""
walkerType = input.split(':')[2]
chromosomes = map(float, input.split(':')[3].split(' '))

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
		if( type == "Quadruped"):
			return QuadrupedController( chromosomes )
		elif( type == "Biped"):
			return BipedController( chromosomes )
		elif( type == "Octoped"):
			return OctopedController( chromosomes )
		elif( type == "SimpleQuadruped"):
			return SimpleQuadrupedController( chromosomes )

	def initWorld( self ):
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
		self.walker.applyJointVelocities( self.getTime() )
		breve.PhysicalControl.iterate( self )
	
WalkerViewer()