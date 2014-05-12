import breve
from WalkerBody import WalkerBody

#TODO remove
BODY_WIDTH = 14
UPPER_LEG_WIDTH = 15
LOWER_LEG_WIDTH = 16
FOOT_WIDTH = 17

NBR_LEGS = 8
LEG_WIDTH = 0.4
ROTATION_NORMAL = breve.vector( 1, 0, 0 )

class OctopedBody( WalkerBody ):
	def __init__( self, chromosomes = None ):
		WalkerBody.__init__( self, chromosomes )

	def setJointVelocities(self, velocities):
		for i in range(0, len( velocities )):
			self.allJoints[i].setJointVelocity( velocities[i] )

	def initShape( self, chromosomes ):
		self.bodyWidth = 2
		self.bodyLength = 8 

		self.legLength = 2

		self.startingHeight = self.legLength * 2

		legShape = breve.Cube().initWith( breve.vector( LEG_WIDTH , LEG_WIDTH , self.legLength ) ) 
		bodyShape = breve.Cube().initWith( breve.vector( self.bodyWidth, self.bodyLength, 0.400000 ) )
	
		self.bodyLink = breve.Link()
		self.legs = breve.createInstances( breve.Links, NBR_LEGS )

		[ link.setShape(legShape) for link in self.legs ]

		self.bodyLink.setShape( bodyShape )

		#Used for resetting the walker position
		self.allLinks = [self.bodyLink] + self.legs 

	def initJoints( self ):
		self.legJoints = breve.createInstances( breve.RevoluteJoints, NBR_LEGS)
		map(self.addDependency, self.legJoints)

		bodyOffsets = []
		for i in range(0, NBR_LEGS):
			if( i < NBR_LEGS / 2):
				widthOffset = self.bodyWidth / 2.0
			else:
				widthOffset = -self.bodyWidth / 2.0

			lengthOffset = -self.bodyLength / 2.0 + self.bodyLength / NBR_LEGS + (i % (NBR_LEGS / 2)) * (self.bodyLength / (NBR_LEGS / 2 - 1))

			bodyOffsets = bodyOffsets + [breve.vector( widthOffset, lengthOffset, 0.2 )]

		#bodyOffsets = [ breve.vector( self.bodyWidth / 2.0 - self.bodyWidth * i // (NBR_LEGS / 2), -self.bodyLength / 2.0 + i * self.bodyLength / (NBR_LEGS / 2), 0.2 ) for i in range( 0, NBR_LEGS )] 

		legOffset = breve.vector( 0, 0, self.legLength / 2.0)
		
		#bodyOffset specifies the point the joints links to on the body, 
		#and upperLegOffset specifies the point on the leg to link to.
		for i in range(0, NBR_LEGS):
			self.legJoints[i].link( ROTATION_NORMAL, bodyOffsets[i], -legOffset, self.legs[ i ], self.bodyLink )
		
		self.legJoints.setDoubleSpring( 700, 0.800000, -0.800000 )

		[ joint.setStrengthLimit( 600 ) for joint in self.legJoints ] #400 innan

		self.allJoints = self.legJoints
		self.setRoot( self.bodyLink )

	def isUpright( self ):
		return self.bodyLink.getRotationMatrix()[5] < 0 