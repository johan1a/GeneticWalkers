import breve
from WalkerBody import WalkerBody

NBR_LEGS = 2
ROTATION_NORMAL = breve.vector( 1, 0, 0 )

class BipedBody( WalkerBody ):
	def __init__( self, chromosomes = None ):
		WalkerBody.__init__( self, chromosomes )

	def setJointVelocities(self, velocities):
		for i in range(0, len( velocities )):
			self.allJoints[i].setJointVelocity( velocities[i] )

	def initShape( self, chromosomes ):
		self.bodyWidth = 4
		self.bodyDepth = 1 
		self.bodyHeight = 4

		footWidth = 2.5
		self.footHeight = 0.3

		self.legLength = 2
		self.legWidth = 0.5

		self.startingHeight = 2 * self.legLength + self.bodyHeight

		lowerLegShape = breve.Cube().initWith( breve.vector( self.legWidth , self.legWidth , self.legLength )) 
		upperLegShape = breve.Cube().initWith( breve.vector( self.legWidth , self.legWidth , self.legLength ))
		footShape = breve.Cube().initWith( breve.vector( footWidth, footWidth, self.footHeight ))
		bodyShape = breve.Cube().initWith( breve.vector( self.bodyWidth, self.bodyDepth, self.bodyHeight ) )
	
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

		left = breve.vector( self.bodyWidth / 2.0, 0, self.bodyHeight/2 )
		right = breve.vector( -self.bodyWidth / 2.0, 0, self.bodyHeight/2 )
		bodyOffsets = [left, right]

		legOffset = breve.vector( 0, 0, self.legLength/2.0)
		footOffset = breve.vector( 0, 0, self.footHeight/2.0)
		
		#bodyOffset specifies the point the joints links to on the body, 
		#and upperLegOffset specifies the point on the leg to link to.
		for i in range(0, NBR_LEGS):
			self.upperLegJoints[i].link( ROTATION_NORMAL, bodyOffsets[i], -legOffset, self.upperLegs[ i ], self.bodyLink )
			self.lowerLegJoints[i].link( ROTATION_NORMAL, legOffset, -legOffset, self.lowerLegs[ i ], self.upperLegs[ i ] )
			self.footJoints[i].link( ROTATION_NORMAL, legOffset + footOffset, breve.vector( 0, 0, 0 ), self.feet[ i ], self.lowerLegs[ i ] )
		
		self.upperLegJoints.setDoubleSpring( 700, 0.800000, -0.800000 )
		self.lowerLegJoints.setDoubleSpring( 700, 0.800000, -0.800000 )
		self.footJoints.setDoubleSpring( 999, 0.400000, -0.400000 ) #kolla

		[ joint.setStrengthLimit( 500 ) for joint in self.allJoints ] #400 innan
		self.setRoot( self.bodyLink )

	def isUpright( self ):
		return self.bodyLink.getRotationMatrix()[5] < -0.1