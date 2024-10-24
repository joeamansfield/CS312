from pickle import TRUE
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



def baseHull(points): #takes 3-5 points sorted left to right, returns hull points sorted clockwise starting at the leftmost point, and index of rightmost point
	right = points[len(points)-1]
	n = len(points)
	noMiddlePoints = []
	for i in range(n):
		for j in range(i+1, n):
			ptsAbove = False
			ptsBelow = False
			partOfHull = True
			m = (points[i].y() - points[j].y()) / (points[i].x() - points[j].x())
			b = points[i].y() - m*points[i].x()
			for k in range(n):
				if k != i and k != j:
					if points[k].y() > m * points[k].x() + b:
						ptsAbove = True
					if points[k].y() < m * points[k].x() + b:
						ptsBelow = True
				if ptsBelow and ptsAbove:
					partOfHull = False
					break
			if partOfHull:
				if noMiddlePoints.count(points[i]) == 0:
					noMiddlePoints.append(points[i])
				if noMiddlePoints.count(points[j]) == 0:
					noMiddlePoints.append(points[j])
	clockwise = []
	clockwise.append(noMiddlePoints.pop(0))
	while len(noMiddlePoints) > 0:
		slope = float("inf") * -1
		maxindex = 0
		for i in range(len(noMiddlePoints)):
			if (noMiddlePoints[i].y()-clockwise[0].y())/(noMiddlePoints[i].x()-clockwise[0].x()) > slope:
				slope = (noMiddlePoints[i].y()-clockwise[0].y())/(noMiddlePoints[i].x()-clockwise[0].x())
				maxindex = i
		clockwise.append(noMiddlePoints.pop(maxindex))
	right = clockwise.index(right)
	return [clockwise, right]

def slope(pt1, pt2):
	rise = pt1.y()-pt2.y()
	run = pt1.x()-pt2.x()
	return rise/run

def mergeHull(leftHull, rightHull):
	leftPts = leftHull[0]
	lenL = len(leftPts)
	rightPts = rightHull[0]
	lenR = len(rightPts)
	leftRight = leftHull[1]
	right = rightPts[rightHull[1]]
	upperR = 0
	upperL = leftRight
	lowerR = 0
	lowerL = leftRight
	lineChanged = True
	while lineChanged:
		lineChanged = False
		if slope(leftPts[upperL], rightPts[upperR]) < slope(leftPts[upperL], rightPts[(upperR+1)%lenR]):
				upperR = (upperR+1)%lenR
				lineChanged = True
		if slope(leftPts[upperL], rightPts[upperR]) > slope(leftPts[(upperL-1)%lenL], rightPts[upperR]):
				upperL = (upperL-1)%lenL
				lineChanged = True
	lineChanged = True
	while lineChanged:
		lineChanged = False
		if slope(leftPts[lowerL], rightPts[lowerR]) > slope(leftPts[lowerL], rightPts[(lowerR-1)%lenR]):
				lowerR = (lowerR-1)%lenR
				lineChanged = True
		if slope(leftPts[lowerL], rightPts[lowerR]) < slope(leftPts[(lowerL+1)%lenL], rightPts[lowerR]):
				lowerL = (lowerL+1)%lenL
				lineChanged = True
	mergePts = leftPts[0: upperL + 1]
	if lowerR == 0:
		mergePts.extend(rightPts[upperR:lenR])
		mergePts.append(rightPts[0])
	else:
		mergePts.extend(rightPts[upperR:lowerR + 1])
	if lowerL != 0:
		mergePts.extend(leftPts[lowerL: lenL])
	right = mergePts.index(right)
	return [mergePts, right]

def solveHullPts(points):
	if len(points) <= 5:
		return baseHull(points)
	else:
		x = round(len(points)/2)
		left = solveHullPts(points[0:x])
		right = solveHullPts(points[x:len(points)])
		return mergeHull(left, right)

def solveHull(points):
	hullPts = solveHullPts(points)[0]
	return [QLineF(hullPts[i],hullPts[(i+1)%len(hullPts)]) for i in range(len(hullPts))]