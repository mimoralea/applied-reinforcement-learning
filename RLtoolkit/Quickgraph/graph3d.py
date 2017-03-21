#<html><body><pre>

## 3DGraphics  combination of 3Dfuncs and surface

# This package creates a 3d graph surface of the data given
"""
graphSurface(window, data, view, color, bounds)
	Draws a 3D surface showing 2d data array.
	view, color and bounds are optional
	if window is None, a window will be created
	graphSurface(window, \
    		[[i*j for i in range(30)] for j in range(30)], \
    	    	 view =(.5 .4 .8),	#view from point given by these fractions of each axis \
    	    	 color='white',		# color to draw surface in \
    	    	window= ((xmin, xmax),(ymin, ymax),(0, 10))   #min and max of each axis.
Examples of use:
   w = Gwindow(windowTitle="3d",gdViewport=(20,20,550,250))
   graphSurface(w, [[i*j for i in range(30)] for j in range(30)])
   or graphSurface(w, func1(30))
Note: if you want your graph to automatically redraw when resized, call graphSurface
   in your gDrawView routine for that window
Doesn't work for arrays less than 5x5 
"""
# if we only have the quickgraph package, use g from that. But if the whole
# toolkit is installed, use g from that

try:
    from RLtoolkit.G.g import *
except:
    from .g import *
    
from math import *
import operator
from functools import reduce

# written by Chuck
# converted to Python by Steph (2004)

hiddenLinesWanted = False
updateYBuffer = True
ySet = [False for i in range(2000)]
yHigh = [0 for i in range(2000)]
yLow = [0 for i in range(2000)]

def set3DSurface (doNotHide, update):
	global hiddenLinesWanted, updateYBuffer
	hiddenLinesWanted = doNotHide
	updateYBuffer = update

def init3DSurface ():
	global ySet
	set3DSurface(False, True)
	for i in range(2000):
		ySet[i] = False

glNumX = 0
glNumY = 0

def g3DSurface (context, data, numx, numy, color):
	global glNumX, glNumY
	glNumX, glNumY = numx, numy
	num = max(numx, numy)
	init3DSurface()
	pieces = []
	for m in range(num - 1):
		pieces.append(drawPart(context, data, num-1, m, num-1, 1+m, color))
		pieces.append(drawPart(context, data, num-1-m, 0, num-2-m, 0, color))
		for i in range(int(round(.5 * (1 + m)))):
			pieces.append(drawPart(context, data, num-2-i, m+1-i, num-2-i, m-i, color))
			pieces.append(drawPart(context, data, num-1-i, m+1-i, num-2-i, m+1-i, color))
			pieces.append(drawPart(context, data, num-2-m+i, i, num-2-m+i, i+1,  color))
			pieces.append(drawPart(context, data, num-1-m+i, i+1, num-2-m+i, i+1, color))
			if ((1+ m) % 2) != 0:
				pieces.append(drawPart(context, data, num-2-m+i, i, num-2-m+i, i+1, color))
				pieces.append(drawPart(context, data, num-2-m+i, i+1, num-1-m+i, i+1, color))
	for mu in range(num - 2):
		m = num - 1 - mu
		for i in range(int(round(.5 * m))):
			pieces.append(drawPart(context, data, m-i-1, num-1-i, m-i-1, num-2-i, color))
			pieces.append(drawPart(context, data, m-i, num-1-i, m-i-1, num-1-i, color))
			pieces.append(drawPart(context, data, i, num-m+i, i, num-m+i+1, color))
			pieces.append(drawPart(context, data, i, num-m+i+1, i+1, num-m+i+1, color))
			if (m % 2) != 0:
				pieces.append(drawPart(context, data, i, num-m+i, i, num-m+i+1, color))
				pieces.append(drawPart(context, data, i, num-m+i+1, i+1, num-m+i+1, color))
	return pieces

def drawPart (context, data, x1, y1, x2, y2, color):
	global glNumX, glNumY
	pieces = []
	if x1 <glNumX and x2 < glNumX and y1 < glNumY and y2 < glNumY:
		a = project3D(x1, y1, data[x1][y1])
		b = project3D(x2, y2, data[x2][y2])
		pieces.append(gDrawProj3DLine(context, a[0], a[1], b[0], b[1], color))
	return pieces

def gDraw3DLine (context, x1, y1, z1, x2, y2, z2, color):
	a = project3D(x1, y1, z1)
	b = project3D(x2, y2, z2)
	return gDrawProj3DLine(context, a[0], a[1], b[0], b[1], color)

def gDrawProj3DLine (context, x1, y1, x2, y2, color):
	global hiddenLinesWanted, updateYBuffer, ySet, yHigh, yLow
	pieces = []
	if hiddenLinesWanted:
		pieces.append(gDrawLine(context, x1, y1, x2, y2, color))
	else:  
		dx1 = gdCoordx(context, x1)
		dy1 = gdCoordy(context, y1)
		dx2 = gdCoordx(context, x2)
		dy2 = gdCoordy(context, y2)
		if dx2 < dx1:						#switch dx1 dx2, and dy1 dy2
			dx1, dx2 = dx2, dx1
			dy1, dy2 = dy2, dy1
		if not dx2 == dx1:
			slope = float(dy2 - dy1) / float(dx2 - dx1)
			intercept = (dy1 - (slope * dx1))
			notvert = True
		else:
			notvert = False
		pendown = False
		x = dx1
		while x <= dx2:
			if x == dx1:
				y = dy1
			elif notvert:
				y = int(round(0.5 + (x * slope) + intercept))
			else:
				y = dy2
			if pendown:
				if covered(x, y):
					ymid =  .5 * (yHigh[x] + yLow[x])
					if y > ymid:
						yc = yHigh[x]
					else:
						yc = yLow[x]
					pieces.append(gdDrawLine (context, xbeg, ybeg, x, yc, color))
					pendown = False
				else:				 ##else not covered
					if updateYBuffer:
						if ySet[x]:
							if y >yHigh[x]:
								yHigh[x] = y
							if y < yLow[x]:
								yLow[x] = y
						else:  ##else not set
							yHigh[x] = yLow[x] = y
							ySet[x] = True
			else:  	##else pen not down
				if not covered(x, y):
					xbeg = x
					if x > 0 and ySet[x - 1] and x != dx1:
						ymid = .5 * (yHigh[x - 1] + yLow[x - 1])
						if y > ymid:
							ybeg = yHigh[x - 1]
						else:
							ybeg = yLow[x - 1]
					else:
						ybeg = y
					pendown = True
					if updateYBuffer:
						if ySet[x]:
							if y > yHigh[x]:
								yHigh[x] = y
							if y < yLow[x]:
								yLow[x] = y
						else:
							yHigh[x] = yLow[x] = y
							ySet[x] = True  
			x += 1
		if pendown:
			if dx1 == dx2:
				y = dy2
			pieces.append(gdDrawLine(context, xbeg, ybeg, dx2, y, color))
	return pieces

def covered (x, y):
	global ySet, yHigh, yLow
	return ySet[x] and y < yHigh[x] and y > yLow[x]

r03D = (1., 0., .7)
u13D = (1., 0., 0.)
u23D = (0., 0., 1.)
u3D = (0., 1., 0.)
distance = .2

###Example use 
#	set3Dprojection(vxgs * numx, vygs * numy, vzgs * wzmaxgs, \
#			   .5 * numx, .5 * numy, .5 * (wzmings + wzmaxgs), numx)
#	window2d = project3Dwindow(wxmings, wxmaxgs, wymings, wymaxgs, wzmings, wzmaxgs)
#	gSetCoordinateSystem(context, window2d[0], window2d[1], window2d[2], window2d[3])

def set3DProjection (r0x, r0y, r0z, rcx, rcy, rcz, d):
	global r03D, u13D, u23D, u3D, distance
	rc = [rcx, rcy, rcz]
	r03D = [r0x, r0y, r0z]
	distance = d
	## u3D is difference between r03D and center of view volumn and normalized
	u3D = normalizeList(list(map(lambda a, b: a-b, r03D, rc)))

	## Rotate (x,y) of u3D 90 degrees to get u13D
	u13D = normalizeList([-u3D[1], u3D[0], 0.])

	## Rotate u3D about (u3D[1], u3D[0], 0) to get u23D
	a, b, c = u3D
	u23D = [ b*b*a - b*a*b - a*c, \
				  a*a*b - b*a*a - b*c, \
				  a*a + b*b ]
  

def project3D (x3D, y3D, z3D):
	global r03D, u13D, u23D, u3D, distance
	rd = list(map(lambda a,b: a-b, [x3D, y3D, z3D], r03D))
	return  [ (-distance * dot(rd, u13D)) / (dot(rd, u3D) - distance), \
				 (-distance * dot(rd, u23D)) / (dot(rd,u3D) - distance) ]

def project3DVector (p3D):
	global r03D, u13D, u23D, u3D, distance
	rd = list(map(lambda a,b: a-b, p3D, r03D))
	return [ (-distance * dot(rd, u13D)) / (dot(rd, u3D) - distance), \
				 (-distance * dot(rd, u23D)) / (dot(rd,u3D) - distance) ]

def project3DWindow (xmin, xmax, ymin, ymax, zmin, zmax):
	corners = ( (xmax, ymin, zmin), \
					 (xmin, ymax, zmin), \
					 (xmax, ymax, zmin), \
					 (xmin, ymin, zmax), \
					 (xmax, ymin, zmax), \
					 (xmin, ymax, zmax), \
					 (xmax, ymax, zmax))
	a = project3DVector ((xmin, ymin, zmin))
	wxmax, wymax = wxmin, wymin = a
	for p in corners:
		a = project3DVector(p)
		x, y = a
		if x < wxmin:
			wxmin = x
		if x > wxmax:
			wxmax = x
		if y < wymin:
			wymin = y
		if y > wymax:
			wymax = y
	return (wxmin, wymin, wxmax, wymax)

def normalizeList(p):
	sum = float(reduce(operator.add, [x * x for x in p]))
	return [float(x) / sum for x in p]
 
def dot (a, b):
	return reduce(operator.add, list(map(lambda x, y: x * y, a, b)))

wxmings = 0
wxmaxgs = 0
wymings = 0
wymaxgs = 0
wzmings = 0
wzmaxgs = 0
vxgs = 0
vygs = 0
vzgs = 0


def graphSurface (context, data, view=(0.55, 0.4, .7), color='white', window=None):   #((None, None),(None, None),(None, None))):
	"""3D surface showing data array.
	graphSurface(view, [[.1, .3, .5],[.3, .2, .1],[.4, .3, .1]],
					 view =(.5 .4 .8),	#view from point given by these fractions of each axis
					color = 'white'    # color to draw surface with
					 window= ((xmin xmax)(ymin ymax)(0 10)))   #min and max of each axis."""
	global hiddenLinesWanted
	if context == None:
		context = Gwindow(windowTitle="3d")
	if view == None:
		view = (0.55, 0.4, 0.7)
	numx = len(data)
	numy = len(data[0])
	bounds = minMaxElement(data)
	#color = gColorWhite(context)
	if window == None:
		wxmings = 0
		wxmaxgs = numx -1
		wymings = 0
		wymaxgs = numy -1
		wzmings = bounds[0]
		wzmaxgs = bounds[1]
	else:
		wxmings = window[0][0]
		wxmaxgs = window[0][1]
		wymings = window[1][0]
		wymaxgs = window[1][1]
		wzmings = window[2][0]
		wzmings = window[2][1]
	vxgs = view[0]
	vygs = view[1]
	vzgs = view[2]
	# Define 3D window.
	pieces =  []
	pieces.append(gClear(context, 'dark blue'))
	set3DProjection( vxgs * numx, vygs * numy, vzgs * wzmaxgs, \
			   .5 * numx, .5 *numy, .5 * (wzmings + wzmaxgs), numx)
	window2d = project3DWindow(wxmings, wxmaxgs, wymings, wymaxgs, wzmings, wzmaxgs)
	gSetCoordinateSystem(context, window2d[0], window2d[1], window2d[2], window2d[3])
	pieces.append(g3DSurface(context, data, numx, numy ,color))
	color = 'yellow'
	pieces.append(gDraw3DLine(context, wxmaxgs, wymaxgs, wzmaxgs, wxmings, wymaxgs, wzmaxgs, color))
	pieces.append(gDraw3DLine(context, wxmaxgs, wymaxgs, wzmaxgs, wxmaxgs, wymaxgs, wzmings, color))
	pieces.append(gDraw3DLine(context, wxmings, wymings, wzmings ,wxmaxgs, wymings, wzmings, color))
	pieces.append(gDraw3DLine(context, wxmings, wymings ,wzmings, wxmings, wymaxgs, wzmings, color))
	pieces.append(gDraw3DLine(context, wxmings, wymings, wzmings, wxmings, wymings, wzmaxgs, color))
	pieces.append(gDraw3DLine(context, wxmings, wymaxgs, wzmaxgs, wxmings, wymings, wzmaxgs, color))
	pieces.append(gDraw3DLine(context, wxmings, wymaxgs, wzmings, wxmaxgs, wymaxgs, wzmings, color))
	pieces.append(gDraw3DLine(context, wxmaxgs, wymings, wzmings, wxmaxgs, wymaxgs, wzmings, color))
	hiddenLinesWanted = True
	pieces.append(gDraw3DLine(context, wxmings, wymaxgs, wzmaxgs, wxmings, wymaxgs, wzmings, color))
	pieces.append(gDraw3DLine(context, wxmaxgs, wymaxgs, wzmaxgs, wxmaxgs, wymings, wzmaxgs, color))
	pieces.append(gDraw3DLine(context, wxmaxgs, wymings, wzmaxgs, wxmaxgs, wymings, wzmings, color))
	pieces.append(gDraw3DLine(context, wxmaxgs, wymings, wzmaxgs, wxmings ,wymings, wzmaxgs, color))
	hiddenLinesWanted = False
	return pieces
	
def minMaxElement (data):
	numx = len(data)
	numy = len(data[0])
	maxv = data[0][0]
	minv = maxv
	for i in range(numx):
		for j in range(numy):
			v = data[i][j]
			if v > maxv:
				maxv = v
			if v < minv:
				minv = v
	maxv = max(maxv, minv + 0.001)
	return [minv, maxv]
"""
# for testing

def func1 (num):
	data = [[0. for j in range(num)] for i in range(num)]
	dx = 2. / (num - 1)
	y = -1.
	for i in range(num):
		x = -1
		for j in range(num):
			data[i][j] = abs(exp(-0.5 * (sqr(x) + sqr(y)))) * (1. + (cos(10. * sqrt(sqr(x) + sqr(y)))))
			x = x + dx
		y = y + dx
	return data

def sqr (x):
	return x * x

w = Gwindow(windowTitle="testing 3d",gdViewport=(20,20,550,250))
#graphSurface(w, [[0 for i in range(3)] for j in range(3)])
graphSurface(w, func1(30))
gStartEventLoop()
"""
#</pre></body></html>
