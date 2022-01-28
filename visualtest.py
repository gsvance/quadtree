#!/usr/bin/env python

# Visual test of the quadtree class

# Last modified 6/28/18 by Greg Vance

import graphics as gr
import quadtree as qt
import random as rn

class VisualQuadTree:
	
	def __init__(self, sideLength):
		center = qt.XY(0.5 * sideLength, 0.5 * sideLength)
		boundary = qt.AABB(center, 0.5 * sideLength)
		self.quadtree = qt.QuadTree(boundary)
		self.win = gr.GraphWin("QuadTree Visual Test", sideLength, sideLength)
		self.win.setBackground("white")
		self.rects = list()
		self.points = list()
		self.selected = list()
	
	def insert(self, p):
		return self.quadtree.insert(p)
	
	def queryRange(self, qrange):
		qresult = self.quadtree.queryRange(qrange)
		self.selected = list()
		for p in qresult:
			point = gr.Point(p.x, p.y)
			point.setFill("orange")
			point.draw(self.win)
			self.selected.append(point)
	
	def unquery(self):
		for point in self.selected:
			point.undraw()
	
	def getRects(self, quadtree):
		rects = list()
		if quadtree == None:
			return rects
		northWestCorner = gr.Point( \
			quadtree.boundary.center.x - quadtree.boundary.halfDimension,
			quadtree.boundary.center.y - quadtree.boundary.halfDimension)
		southEastCorner = gr.Point( \
			quadtree.boundary.center.x + quadtree.boundary.halfDimension,
			quadtree.boundary.center.y + quadtree.boundary.halfDimension)
		rect = gr.Rectangle(northWestCorner, southEastCorner)
		rect.setOutline("blue")
		rects.append(rect)
		rects.extend(self.getRects(quadtree.northWest))
		rects.extend(self.getRects(quadtree.northEast))
		rects.extend(self.getRects(quadtree.southWest))
		rects.extend(self.getRects(quadtree.southEast))
		return rects
	
	def getPoints(self, quadtree):
		points = list()
		if quadtree == None:
			return points
		for p in quadtree.points:
			point = gr.Point(p.x, p.y)
			point.setFill("black")
			points.append(point)
		points.extend(self.getPoints(quadtree.northWest))
		points.extend(self.getPoints(quadtree.northEast))
		points.extend(self.getPoints(quadtree.southWest))
		points.extend(self.getPoints(quadtree.southEast))
		return points
	
	def draw(self):
		self.rects = self.getRects(self.quadtree)
		self.points = self.getPoints(self.quadtree)
		for rect in self.rects:
			rect.draw(self.win)
		for point in self.points:
			point.draw(self.win)
	
	def undraw(self):
		for rect in self.rects:
			rect.undraw()
		for point in self.points:
			point.undraw()

tree = VisualQuadTree(800)

tree.draw()

click = tree.win.getMouse()
qcenter = qt.XY(click.getX(), click.getY())

click = tree.win.getMouse()
qhalfDimension = max(abs(qcenter.x - click.getX()), 
	abs(qcenter.y - click.getY()))

qrange = qt.AABB(qcenter, qhalfDimension)

qnorthWest = gr.Point(qcenter.x - qhalfDimension, qcenter.y - qhalfDimension)
qsouthEast = gr.Point(qcenter.x + qhalfDimension, qcenter.y + qhalfDimension)
qrect = gr.Rectangle(qnorthWest, qsouthEast)
qrect.setOutline("red")

qrect.draw(tree.win)
tree.queryRange(qrange)

while True:
	
	tree.undraw()
	qrect.undraw()
	tree.unquery()
	
	p = qt.XY(click.getX(), click.getY())
	tree.insert(p)
	
	tree.draw()
	qrect.draw(tree.win)
	tree.queryRange(qrange)
	
	#click = tree.win.getMouse()
	click = gr.Point(800 * rn.random(), 800 * rn.random())

