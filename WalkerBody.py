import breve


#TODO remove
BODY_WIDTH = 14
UPPER_LEG_WIDTH = 15
LOWER_LEG_WIDTH = 16
FOOT_WIDTH = 17

NBR_LEGS = 4
LEG_WIDTH = 0.4
FOOT_HEIGHT = 0.2
ROTATION_NORMAL = breve.vector( 1, 0, 0 )

class WalkerBody( breve.MultiBody ):
	def __init__( self ):
		breve.MultiBody.__init__( self )
		self.initShape( [1]*18 ) 
		self.initJoints()

	def setJointVelocities(self, velocities):
		s = 3
		for i in range(0, len( velocities )):
			self.allJoints[i].setJointVelocity( velocities[i] )

	def center( self ):
		self.move( breve.vector( 0, self.upperLegLength + self.lowerLegLength + self.footHeight + 5, 0 ) )
		self.rotate( breve.vector( 1, 0, 0 ), 1.570000 )
		for joint in self.allJoints:
			joint.setJointVelocity(0)

	def setColors( self, colors ):
		self.allLinks[0].setColor(colors[0])
		[link.setColor(colors[1]) for link in self.allLinks[1:]]

	def initBody( self, chromosomes ):
		[ breve.deleteInstances( link ) for link in self.allLinks ]
		[ breve.deleteInstances( joint ) for joint in self.allJoints ]

		self.initShape(chromosomes)
		self.initJoints()

	def initShape( self, chromosomes ):

		self.bodyWidth = chromosomes[BODY_WIDTH]
		self.bodyLength = self.bodyWidth # might remove

		footWidth = chromosomes[FOOT_WIDTH]
		self.footHeight = FOOT_HEIGHT

		self.upperLegLength = chromosomes[UPPER_LEG_WIDTH]

		self.lowerLegLength = chromosomes[LOWER_LEG_WIDTH]

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
		ROTATION_NORMAL = breve.vector( 1, 0, 0 )
		
		#bodyOffset specifies the point the joints links to on the body, 
		#and upperLegOffset specifies the point on the leg to link to.
		for i in range(0, NBR_LEGS):
			self.upperLegJoints[i].link( ROTATION_NORMAL, bodyOffsets[i], -upperLegOffset, self.upperLegs[ i ], self.bodyLink )
			self.lowerLegJoints[i].link( ROTATION_NORMAL, upperLegOffset, -lowerLegOffset, self.lowerLegs[ i ], self.upperLegs[ i ] )
			self.footJoints[i].link( ROTATION_NORMAL, lowerLegOffset + footOffset, breve.vector( 0, 0, 0 ), self.feet[ i ], self.lowerLegs[ i ] )
		
		self.upperLegJoints.setDoubleSpring( 700, 0.800000, -0.800000 )
		self.lowerLegJoints.setDoubleSpring( 700, 0.800000, -0.800000 )
		self.footJoints.setDoubleSpring( 700, 0.800000, -0.800000 ) #kolla

		[ joint.setStrengthLimit( 400 ) for joint in self.allJoints ]
		self.setRoot( self.bodyLink )

	def isUpright( self ):
		return self.bodyLink.getRotationMatrix()[5] < 0 