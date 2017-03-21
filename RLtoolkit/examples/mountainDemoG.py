# This is an example program for reinforcement learning with linear function
# approximation. The learning algorithm used is sarsa(lambda) with traces.

# This is the GUI version of mountain car. Simply import/load it and it will
# display a graphical interface to the mountain car simulation. You can run
# episodes from there.

# Written by Rich Sutton 12/17/00
# Converted to Python in April, 2004
# Modified to use the RL interface in April 2004

from .mountainEnv import *
from .mountainAgent import *
from RLtoolkit.RLinterface import RLinterface
from RLtoolkit.guiwindow import *
from RLtoolkit.G.g import *
from RLtoolkit.Quickgraph.graph3d import *

# Graphical display routines 

class MCarWindow (SimulationWindow):

    def __init__(self, wwidth=340, wheight=660):
        global mcarTopView, mcarSideView, GDEVICE
        gwidth = GDEVICE.wwidth
        gheight = GDEVICE.wheight
        if wheight >= gheight:
            wwidth = int((gheight - 100) / float(wheight) * wwidth)
            wheight = gheight - 100
        SimulationWindow.__init__(self, wwidth, wheight)
        gSetTitle(self, "Mountain Car")
        self.rlsim = RLinterface(mountainAgent, mountainEnv)
        gSetCS(self, 0, 20, 340, 680, 'lowerLeft')
	mcarTopView = Gview(self)
	gSetViewport(mcarTopView, 20, 360, 320, 660)
	gSetCS(mcarTopView, minPosition, -maxVelocity, maxPosition, maxVelocity)
	mcarSideView = Gview(self)
	gSetViewport(mcarSideView, 20, 100, 320, 345)
	gSetCS(mcarSideView, minPosition, -1.1, maxPosition, 1.1)
	gClear(self, 'blue')
        
    def wholeSimDisplay(self):
        oldep = self.episodenum
        self.stepnum, self.episodenum, self.episodestepnum = curStats()
        if self.episodestepnum == 0 or self.episodenum != oldep:
            drawMcarView()
        else:
            position, velocity, lasta = curState()
            drawMcarState(position, velocity, lasta)
        g3dUpdate()
        gMakeVisible(self) 

    def updateSimDisplay(self):
        oldep = self.episodenum
        self.stepnum, self.episodenum, self.episodestepnum = curStats()
        if self.episodestepnum == 0 or self.episodenum != oldep:
            drawMcarView()
        else:
            position, velocity, lasta = curState()
            drawMcarState(position, velocity, lasta)
        gMakeVisible(self) 

    def resetSimulation(self):
        global mcarSideView, mcarTopView, g3dwindow
	setupAgent()
	setupEnv()
	self.stepnum, self.episodenum,self.episodestepnum = curStats()
	self.wholeView()

displays = displayt = []

def drawMcarView():
    global mcarSideView, mcarTopView, minPosition, maxPosition, maxVelocity, \
           displays, displayt
    gDelete(mcarSideView, displays)
    gDelete(mcarTopView, displayt)
    displays = displayt = []
    position, velocity, lasta = curState()
    displays.append(gClear(mcarSideView, 'blue'))  
    displayt.append(gClear(mcarTopView, 'purple'))
    displayt.append(gFillRect(mcarTopView, goalPosition, -maxVelocity, \
                              maxPosition, maxVelocity, 'green'))
    displayt.append(gDrawLine(mcarTopView, minPosition, 0, maxPosition, 0, 'light gray'))

    # draw mountain
    lasty = lastx = None
    radius, delta = 0.09, 0.01
    pos = minPosition
    for i in range(int((maxPosition - minPosition) / delta)):
        slope = mCarSlope(pos)
        angle = atan(slope)
        x = pos + (radius * sin(angle))
        y = mCarHeight(pos) - (radius * cos(angle))
        if lastx != None:
            displays.append(gDrawLine(mcarSideView, lastx, lasty, x, y, 'white'))
        lastx = x
        lasty = y
        pos += delta
    displays.append(gDrawLineR(mcarSideView, goalPosition, \
                               mCarHeight(goalPosition) - 0.09, 0, -.1, 'white'))
    drawMcarState(position, velocity, lasta)

oldtop = []

def drawMcarState(pos, vel, lasta):
    global mcarTopView, oldtop, displayt
    tsteps, e, esteps = curStats()
    gDelete(mcarTopView, oldtop)
    oldtop = []
    oldtop.append(gDrawDisk(mcarTopView, pos, vel, .033, 'white'))   
    displayt.append(gDrawPoint(mcarTopView, pos, vel, 'white'))
    #if esteps % 10 == 0 or pos >= goalPosition:
    drawMcarSide(pos, vel, lasta)
    #if steps != 0 and (steps % 100 == 0 or pos >= goalPosition):
    #	g3dUpdate()

oldside = []

def drawMcarSide(showpos, showvel, lasta):
    global mcarSideView, minPosition, maxPosition, maxVelocity, oldside
    # erase previous disk and arrow
    gDelete(mcarSideView, oldside)
    h = mCarHeight(showpos)
    oldside = []
    oldside.append(gDrawDisk(mcarSideView, showpos, h, 0.065, 'white'))  
    d = .1
    if lasta == 2:
        oldside.append(gDrawArrow(mcarSideView, showpos+d, h, showpos+d+d, h, 'white'))   
    elif lasta == 0:
        oldside.append(gDrawArrow(mcarSideView, showpos-d, h, showpos-d-d, h, 'white'))    
            
class G3Dwindow (Gwindow):
    def __init__(self, **kwargs):
        Gwindow.__init__(self, **kwargs)
        self.res = 30
        self.data = [[0 for i in range(30)] for j in range(30)]
        gdAddButton(self, "update", g3dUpdate, 5, 5, 'dark blue')
        self.grbits = []
            
    def gDrawView(self):
        gDelete(self, self.grbits)
        self.grbits = graphSurface(self, self.data)
        gMakeVisible(self)

    def gDestroy(self, event):  # quit if this is last window 
        global GDEVICE
        Gwindow.gDestroy(self, event)
        if GDEVICE.childwindows == []:
            gQuit()

g3dwindow = None

def g3dGraph (resolution=30):
    "Draws the state-value function in a 3d graph in a separate window"
    global g3dwindow
    g3dwindow = G3Dwindow(windowTitle="State-value Function")
    gdSetViewportR(g3dwindow, 350, 20, 400, 400)
    if resolution != g3dwindow.res:
        g3dwindow.res = resolution
    g3dwindow.data = [[0 for i in range(resolution)] for j in range(resolution)]
    g3dwindow.gDrawView()

def calcD(Fs):
    "calculate distances for 3d window"
    global theta, m
    d = -100.0
    for a in range(m):
	s = 0.0
	for v in Fs[a]:
	    s += theta[v]
	if s > d:
	    d = s
    return d

def g3dUpdate():
    global g3dwindow, minPosition, maxPosition, maxVelocity, m, theta, numTilings
    global posWidth, velWidth
    Fs = [[0 for item1 in range(numTilings)] for item2 in range(m)]
    for i in range(g3dwindow.res):
        pos = minPosition + ((maxPosition - minPosition) * (float(i) / (g3dwindow.res-1)))
        for j in range(g3dwindow.res):
            vel = (2 * maxVelocity * (float(j) / (g3dwindow.res-1))) - maxVelocity
            loadF(Fs, pos, vel)
            if mCarGoal(pos):
                d = 0.0
            else:
                d = calcD(Fs)
            g3dwindow.data[i][j] = d
    g3dwindow.gDrawView()

def initMCdisplay():
    global mcarWindow, mcarTopView, mcarSideView
    mcarWindow = MCarWindow()
    drawMcarView()
    g3dGraph()

def runDemo():
    initMCdisplay()
    gMainLoop()

if __name__ == '__main__':
    runDemo()
