import breve
class WalkerBody( breve.MultiBody ):
	def __init__( self ):
		breve.MultiBody.__init__( self )
		self.nbrLegs = 4
		self.bodyWidth = 4
		self.bodyLength = 4

		self.initShapes()
		self.initJoints()
		self.center()

	def setJointVelocities(self, velocities):
		for i in range(0, len(self.joints)):
			self.joints[i].setJointVelocity(velocities[i])

	def center( self ):
		self.move( breve.vector( 0, self.upperLegLength*2+0.5, 0 ) )
		self.rotate( breve.vector( 1, 0, 0 ), 1.570000 )
		for joint in self.joints:
			joint.setJointVelocity(0)

	def setColors( self, colors ):
		for i in range(0,2):
			self.upperLegs[2 * i].setColor( colors[i] )
			self.lowerLegs[2 * i].setColor( colors[i] )
			self.upperLegs[2 * i + 1].setColor( colors[i] )
			self.lowerLegs[2 * i + 1].setColor( colors[i] )

	def initShapes( self ):
		lowerLegWidth = 0.4
		lowerLegLength = 1
		upperLegWidth = 0.4
		self.upperLegLength = 1

		lowerLegShape = breve.Cube().initWith( breve.vector( lowerLegWidth, lowerLegWidth, lowerLegLength )) 
		upperLegShape = breve.Cube().initWith( breve.vector( upperLegWidth, upperLegWidth, self.upperLegLength ))
		bodyShape = breve.Cube().initWith( breve.vector( self.bodyWidth, self.bodyLength, 0.400000 ) )
	
		self.bodyLink = breve.Link()
		self.lowerLegs = breve.createInstances( breve.Links, self.nbrLegs )
		self.upperLegs = breve.createInstances( breve.Links, self.nbrLegs )

		[ link.setShape(upperLegShape) for link in self.upperLegs ]
		[ link.setShape(lowerLegShape) for link in self.lowerLegs ]

		self.bodyLink.setShape( bodyShape )

	def initJoints( self ):
		self.joints = breve.createInstances( breve.RevoluteJoints, self.nbrLegs * 2 )
		map(self.addDependency,self.joints)		

		rearLeft = breve.vector( self.bodyWidth / 2.0, -self.bodyLength / 2.0, 0.4 )
		frontLeft = breve.vector( self.bodyWidth / 2.0, self.bodyLength / 2.0, 0.4 )
		rearRight = breve.vector( -self.bodyWidth / 2.0, -self.bodyLength / 2.0, 0.4 )
		frontRight = breve.vector( -self.bodyWidth / 2.0, self.bodyLength / 2.0, 0.4 )
		bodyOffsets = [frontLeft, frontRight, rearLeft, rearRight]

		legOffsetPos = breve.vector( 0, 0, self.upperLegLength/2.0)
		legOffsetNeg = -legOffsetPos
		legOffsets = [legOffsetPos, legOffsetNeg]

		rotNormal = breve.vector( 1, 0, 0 )
		#bodyOffset specifies the point the joints links to on the body, 
		#and legOffset specifies the point on the leg to link to.
		for i in range(0,4):
			self.joints[ 2 * i ].link( rotNormal, bodyOffsets[i], legOffsets[1], self.upperLegs[ i ], self.bodyLink )
			self.joints[ 2 * i + 1 ].link( rotNormal, legOffsets[0], legOffsets[1], self.lowerLegs[ i ], self.upperLegs[ i ] )

		self.joints.setDoubleSpring(400, 0.800000, -0.800000 )
		self.joints.setStrengthLimit( 400 )
		self.setRoot( self.bodyLink )