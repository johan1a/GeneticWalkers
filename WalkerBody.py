import breve

class WalkerBody( breve.MultiBody ):
	def __init__( self , chromosomes = None):
		breve.MultiBody.__init__( self )
		self.allLinks = None
		self.allJoints = None

	def setJointVelocities(self, velocities):
		s = 3
		for i in range(0, len( velocities )):
			self.allJoints[i].setJointVelocity( velocities[i] )

	def center( self ):
		self.move( breve.vector( 0, self.startingHeight, 0 ) )
		self.rotate( breve.vector( 1, 0, 0 ), 1.570000 )
		for joint in self.allJoints:
			joint.setJointVelocity(0)

	def setColors( self, colors ):
		self.allLinks[0].setColor(colors[0])
		[link.setColor(colors[1]) for link in self.allLinks[1:]]

	def deleteBody( self ):
		[ breve.deleteInstances( link ) for link in self.allLinks ]
		[ breve.deleteInstances( joint ) for joint in self.allJoints ]

	def initBody( self, chromosomes ):
		self.initShape( chromosomes )
		self.initJoints()