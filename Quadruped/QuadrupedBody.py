import breve
from WalkerBody import WalkerBody

#TODO remove
BODY_WIDTH = 14
UPPER_LEG_WIDTH = 15
LOWER_LEG_WIDTH = 16
FOOT_WIDTH = 17

NBR_LEGS = 4
LEG_WIDTH = 0.4
FOOT_HEIGHT = 0.2
ROTATION_NORMAL = breve.vector( 1, 0, 0 )

class QuadrupedBody( WalkerBody ):
	def __init__( self, chromosomes = None ):
		WalkerBody.__init__( self, chromosomes )

	def setJointVelocities(self, velocities):
		for i in range(0, len( velocities )):
			self.allJoints[i].setJointVelocity( velocities[i] )

	def initShape( self, chromosomes ):
		self.bodyWidth = chromosomes[BODY_WIDTH]
		self.bodyLength = self.bodyWidth # might remove

		footWidth = chromosomes[FOOT_WIDTH]
		self.footHeight = FOOT_HEIGHT

		self.upperLegLength = chromosomes[UPPER_LEG_WIDTH]
		self.lowerLegLength = chromosomes[LOWER_LEG_WIDTH]

		self.startingHeight = self.upperLegLength + self.lowerLegLength + self.footHeight + 5

		lowerLegShape = breve.Cube().initWith( breve.vector( LEG_WIDTH , LEG_WIDTH , self.lowerLegLength )) 
		upperLegShape = breve.Cube().initWith( breve.vector( LEG_WIDTH , LEG_WIDTH , self.upperLegLength ))
		footShape = breve.Cube().initWith( breve.vector( footWidth, footWidth, self.footHeight ))
		bodyShape = breve.Cube().initWith( breve.vector( self.bodyWidth, self.bodyWidth, 0.400000 ) )
	
		self.bodyLink = breve.Link()
		self.lowerLegs = breve.createInstances( breve.Links, NBR_LEGS )
		self.upperLegs = breve.createInstances( breve.Links, NBR_LEGS )
		self.feet = breve.createInstances( breve.Links, NBR_LEGS )

		[ link.setShape(upperLegShape) for link in self.upperLegs ]
		[ link.setShape(lowerLegShape) for link in self.lowerLegs ]
		[ link.setShape(footShape) for link in self.feet ]

		self.bodyLink.setShape( bodyShape )

		#Used for resetting the walker position
		self.allLinks = [self.bodyLink] + self.upperLegs + self.lowerLegs + self.feet

	def initJoints( self ):
		self.upperLegJoints = breve.createInstances( breve.RevoluteJoints, NBR_LEGS)
		self.lowerLegJoints = breve.createInstances( breve.RevoluteJoints, NBR_LEGS)
		self.footJoints = breve.createInstances( breve.RevoluteJoints, NBR_LEGS)

		self.allJoints = self.upperLegJoints + self.lowerLegJoints + self.footJoints
		map(self.addDependency, self.allJoints)

		rearLeft = breve.vector( self.bodyWidth / 2.0, -self.bodyLength / 2.0, 0.2 )
		frontLeft = breve.vector( self.bodyWidth / 2.0, self.bodyLength / 2.0, 0.2 )
		rearRight = breve.vector( -self.bodyWidth / 2.0, -self.bodyLength / 2.0, 0.2 )
		frontRight = breve.vector( -self.bodyWidth / 2.0, self.bodyLength / 2.0, 0.2 )
		bodyOffsets = [frontLeft, frontRight, rearLeft, rearRight]

		upperLegOffset = breve.vector( 0, 0, self.upperLegLength/2.0)
		lowerLegOffset = breve.vector( 0, 0, self.lowerLegLength/2.0)
		footOffset = breve.vector( 0, 0, self.footHeight/2.0)
		
		#bodyOffset specifies the point the joints links to on the body, 
		#and upperLegOffset specifies the point on the leg to link to.
		for i in range(0, NBR_LEGS):
			self.upperLegJoints[i].link( ROTATION_NORMAL, bodyOffsets[i], -upperLegOffset, self.upperLegs[ i ], self.bodyLink )
			self.lowerLegJoints[i].link( ROTATION_NORMAL, upperLegOffset, -lowerLegOffset, self.lowerLegs[ i ], self.upperLegs[ i ] )
			self.footJoints[i].link( ROTATION_NORMAL, lowerLegOffset + footOffset, breve.vector( 0, 0, 0 ), self.feet[ i ], self.lowerLegs[ i ] )
		
		self.upperLegJoints.setDoubleSpring( 700, 0.800000, -0.800000 )
		self.lowerLegJoints.setDoubleSpring( 700, 0.800000, -0.800000 )
		self.footJoints.setDoubleSpring( 700, 0.800000, -0.800000 ) #kolla

		[ joint.setStrengthLimit( 500 ) for joint in self.allJoints ] #400 innan
		self.setRoot( self.bodyLink )

	def isUpright( self ):
		return self.bodyLink.getRotationMatrix()[5] < 0 