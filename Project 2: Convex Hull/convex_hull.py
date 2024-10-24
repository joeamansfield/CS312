from re import X
from tkinter import Y
from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT6':
	from PyQt6.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))
import time
from Hull_algorithms import *

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False

# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseHull(self,polygon):
		self.view.clearLines(polygon)

	def showText(self,text):
		self.view.displayStatusText(text)


# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )
		t1 = time.time()
		def pointMerge(points1, points2):
			merged = []
			while(len(points1) > 0 or len(points2) > 0):
				if len(points1) > 0 and len(points2) > 0:
					if points1[0].x() < points2[0].x():
						merged.append(points1.pop(0))
					else:
						merged.append(points2.pop(0))
				else:
					if len(points1) > 0:
						merged.append(points1.pop(0))
					if len(points2) > 0:
						merged.append(points2.pop(0))
			return merged
		def pointMergeSort(points):
			if len(points) > 1:
				x = pointMergeSort(points[0: round(len(points)/2)])
				y = pointMergeSort(points[round(len(points)/2): len(points)])
				return pointMerge(x, y)
			else:
				return points
		points = pointMergeSort(points)
		# TODO: SORT THE POINTS BY INCREASING X-VALUE
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		polygon = solveHull(points)
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
