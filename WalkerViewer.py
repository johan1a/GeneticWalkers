import breve, os

srcDir = sys.path[-2]
print srcDir
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





FILE_NAME = "walkersToView.txt"
INTERVAL = 30
class WalkerViewer( breve.PhysicalControl ):
	def __init__( self ):
		print "Starting program..."
		breve.PhysicalControl.__init__( self )
		self.walker = None
		self.loadInput()
		self.currentWalkerIndex = 0
		self.initWalker()
		self.initWorld()

		

	def initWalker( self ):
		if(self.currentWalkerIndex < len(self.walkerData)):
			if(self.walker):
				self.walker.deleteBody()
			data = self.walkerData[self.currentWalkerIndex]
			walkerType = data[1]
			generation = data[0]

			if(walkerType == "Biped" or generation == "0" ):
				interval = 10
			else:
				interval = INTERVAL
			self.walker = self.makeWalker( walkerType, data[2] )
			self.walker.setupBody()

			text = walkerType + " Generation #" + generation
			self.setDisplayText( text , -0.95, -0.9 )

			
			self.watch( self.walker.getBody() )
			self.currentWalkerIndex = self.currentWalkerIndex + 1
			self.schedule( 'initWalker', ( self.getTime() + interval ) )
		else:
			self.currentWalkerIndex = 0
			self.initWalker()
		

	def loadInput( self ):
		f = open(srcDir + '\\' + FILE_NAME, 'r')
		inputData = f.readlines()
		self.loadWalkers( inputData )
		f.close()

	def loadWalkers( self, inputData ):
		self.walkerData = []
		for line in inputData:
			if( ':' in line ):
				splitString = line.split(':')
				generation = splitString[1]
				walkerType = splitString[2]
				chromosomes = map(float, splitString[3].split(' '))
				self.walkerData = self.walkerData + [( generation, walkerType, chromosomes )]

	def makeWalker( self, walkerType, chromosomes):
		if( walkerType == "Quadruped"):
			return QuadrupedController( chromosomes )
		elif( walkerType == "Biped"):
			return BipedController( chromosomes )
		elif( walkerType == "Octoped"):
			return OctopedController( chromosomes )
		elif( walkerType == "SimpleQuadruped"):
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
		self.enableReflections()
		self.setBackgroundColor( breve.vector( 0.4, 0.6, 0.9 ) )
		self.setBackgroundTextureImage( self.cloudTexture )

		self.offsetCamera( breve.vector( 14, 12, -14 ) )

	def iterate( self ):
		self.walker.applyJointVelocities( self.getTime() )
		breve.PhysicalControl.iterate( self )
	
WalkerViewer()