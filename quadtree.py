# Python module with a quadtree class for testing

# Last modified 6/28/18 by Greg Vance

class XY:

	def __init__(self, x, y):
		self.x = x
		self.y = y

class AABB:
	
	def __init__(self, center, halfDimension):
		self.center = center
		self.halfDimension = halfDimension
	
	def containsPoint(self, point):
		return (point.x >= self.center.x - self.halfDimension \
			and point.x <= self.center.x + self.halfDimension \
			and point.y >= self.center.y - self.halfDimension \
			and point.y <= self.center.y + self.halfDimension)
	
	def intersectsAABB(self, other):
		return not (self.center.x - self.halfDimension \
			> other.center.x + other.halfDimension \
			or self.center.x + self.halfDimension \
			< other.center.x - other.halfDimension \
			or self.center.y - self.halfDimension \
			> other.center.y + other.halfDimension \
			or self.center.y + self.halfDimension \
			< other.center.y - other.halfDimension)

QT_NODE_CAPACITY = 4

class QuadTree:
	
	def __init__(self, boundary):
		self.boundary = boundary
		self.points = list()
		self.northWest = None
		self.northEast = None
		self.southWest = None
		self.southEast = None
	
	def insert(self, p):
		if not self.boundary.containsPoint(p):
			return False
		if len(self.points) < QT_NODE_CAPACITY:
			self.points.append(p)
			return True
		if self.northWest == None:
			self.subdivide()
		if self.northWest.insert(p):
			return True
		if self.northEast.insert(p):
			return True
		if self.southWest.insert(p):
			return True
		if self.southEast.insert(p):
			return True
		return False
	
	def subdivide(self):
		quarterDimension = 0.5 * self.boundary.halfDimension
		northWestCenter = XY(self.boundary.center.x - quarterDimension,
			self.boundary.center.y - quarterDimension)
		self.northWest = QuadTree(AABB(northWestCenter, quarterDimension))
		northEastCenter = XY(self.boundary.center.x + quarterDimension,
			self.boundary.center.y - quarterDimension)
		self.northEast = QuadTree(AABB(northEastCenter, quarterDimension))
		southWestCenter = XY(self.boundary.center.x - quarterDimension,
			self.boundary.center.y + quarterDimension)
		self.southWest = QuadTree(AABB(southWestCenter, quarterDimension))
		southEastCenter = XY(self.boundary.center.x + quarterDimension,
			self.boundary.center.y + quarterDimension)
		self.southEast = QuadTree(AABB(southEastCenter, quarterDimension))
	
	def queryRange(self, qrange):
		pointsInRange = list()
		if not self.boundary.intersectsAABB(qrange):
			return pointsInRange
		for p in xrange(len(self.points)):
			if qrange.containsPoint(self.points[p]):
				pointsInRange.append(self.points[p])
		if self.northWest == None:
			return pointsInRange
		pointsInRange.extend(self.northWest.queryRange(qrange))
		pointsInRange.extend(self.northEast.queryRange(qrange))
		pointsInRange.extend(self.southWest.queryRange(qrange))
		pointsInRange.extend(self.southEast.queryRange(qrange))
		return pointsInRange

