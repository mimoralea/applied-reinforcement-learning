"""Gui code for gridworld with objects/rewards
This code is based on the general gridworld GUI code in gwguimain. It specializes
both the gridworld gui object and the simulation object.
Note: negative consumable rewards may not disappear when they are consumed until
the square is redrawn for some other reason.
"""

from RLtoolkit.g import *
from .gwguimain import *
import operator

class ObjectGridworldView (ObjectGridworld, GridworldView):

    def __init__(self, parent, width=None, height=None, \
                 startsquare=None, goalsquare=None, squaresize=60):
        GridworldView.__init__(self, parent, width, height, \
                               startsquare, goalsquare, squaresize)
        ObjectGridworld.__init__(self, width, height, startsquare, goalsquare)
        self.clickBarrier = True
        self.curvalue = 1.0
        self.curtype = 'permanent'
        self.lowObjValue = -1.0
        self.highObjValue = 1.0
        self.objIncr = 0.1

    def handleSquareClick (self, agent, square):    # click can add barrier or object, not just barrier
        if not self.clickBarrier:                      # add or remove object
            if self.objects[square] != None:
                self.removeObject(square)
            else:
                self.addObject(square, self.curvalue, self.curtype)
            self.squareDrawContents(agent, square)
        else:                                       # toggle barrier status of square
            self.toggleBarrier(square)
            self.squareDrawContents(agent, square)
        
    def squareDrawMore (self, agent, square):       # draw objects
        if self.objects[square] != None:
            self.contents[square].append(self.drawObject(agent, square, \
                                                         self.objects[square]))

    def drawObject(self, agent, square, objectrep):
        if isinstance(objectrep, (tuple, list)):
            return self.gFillObject(square, objectrep[1], objectrep[0])
        else:
            return self.gFillObject(square, objectrep)

    def objectColor (self, value):
        # want value between 0 and 511 (0 to 254 negative, 255 0, 256 to 511 positive)
        value = value / self.highObjValue
        i = 255 + int(minmax(value, -1, 1) * 255)
        return self.colors[i]
       
    def gFillObject (self, square, value, otype = 'permanent'):
        mid = self.squaresize // 2
        dx = self.squaredh(square) 
        dy = self.squaredv(square) 
        color = self.objectColor(value)
        radius = self.squaresize // 3
        if otype == 'permanent':
            return gdDrawDisk(self, dx+mid+1, dy+mid+1, radius, color), \
                   gdDrawCircle(self, dx+mid+1, dy+mid+1, radius, 'black')
        else:  #consumable
            return gdDrawWedge(self, dx+mid+1, dy+mid+radius, 2*radius, 50, 80, color), \
                   gdDrawArc(self, dx+mid+1, dy+mid+radius, 2*radius, 50, 80, 'black')

class ObjectGridworldWindow (GridworldWindow):

    def __init__(self, width=None, height=None, startsquare=None, goalsquare=None, squaresize=None):
        GridworldWindow.__init__(self, width, height, startsquare, goalsquare, squaresize, ObjectGridworldView)
        x1, y1, x2, y2 = gdGetViewport(self)
        gdSetViewport(self, x1, y1, x2, y2+30)   # add enough for buttons
        buttony = self.wheight - 30
        self.addbutton = gdAddButton(self, "Click means barrier", self.setObject, 5, buttony) 
        gSetTitle(self, "Object Gridworld Simulation")
        gdAddButton(self, "-", self.decrObjValue, 170, buttony) 
        self.valbutton = gdAddButton(self, "1.0", None, 210, buttony) 
        gdAddButton(self, "+", self.incrObjValue, 270, buttony) 
        self.typebutton = gdAddButton(self, 'permanent', self.changeType, 320, buttony) 
        self.addObjectMenu()

    def makeNewSimulation(self, w=16, h=16, st=0, g=1, size=30, agentclass=DynaGridAgent):
        s = ObjectGridworldWindow(width=w, height=h, startsquare=st, goalsquare=g, squaresize=size)
        env = s.gridview
        agent = agentclass(numstates=env.numsquares, numactions=env.numactions())
        simInit(s, agent, env, False)
        return s

    def readFile(self, filename):
        if filename != None and filename != '':       
            list = readGridworld(filename)
            gridworld = self.genGridworld(list)
            setWindowTitleFromNamestring(gridworld, filename)

    def writeFile(self, filename):
        olist = prepareWrite(self.gridview)
        olist['objects'] = strlist(self.gridview.objects) #str(self.gridview.objects)
        writeGridworld(olist, filename)

    def genGridworld(self, alist, agentclass=DynaGridAgent):
        width, height, startsquare, goalsquare, barrierp, wallp = getgwinfo(alist)
        squaresize = alist.get('squaresize')
        objects = alist.get('objects')
        gridworld = ObjectGridworldWindow (width, height, startsquare, goalsquare, squaresize)
        gview = gridworld.gridview
        if barrierp != None:
            gview.barrierp = barrierp
        if wallp != None:
            gview.wallp = wallp
        if objects != None:
            gview.objects = objects
        gview.updatedisplay = True
        agent = agentclass(numstates=gview.numsquares, numactions=gview.numactions())
        simInit(gridworld, agent, gview, False)
        return gridworld

    def setObject(self):
        "toggle between clicks meaning barriers and clicks meaning objects"
        if self.gridview.clickBarrier:
            self.setClickObject()
        else:
            self.setClickBarrier()

    def changeType(self):
        "toggle between permanent and consumable objects"
        if self.gridview.curtype == 'permanent':
            self.gridview.curtype = 'consumable'
        else:
            self.gridview.curtype = 'permanent'
        gSetTitle(self.typebutton, self.gridview.curtype)

    def setClickBarrier(self):
        self.gridview.clickBarrier = True
        gSetTitle(self.addbutton, "Click means barrier")

    def setClickObject(self):
        self.gridview.clickBarrier = False
        gSetTitle(self.addbutton, "Click means object")

    def incrObjValue(self):
        self.gridview.curvalue += self.gridview.objIncr
        gSetTitle(self.valbutton, str(round(self.gridview.curvalue, 1)))

    def decrObjValue(self):
        self.gridview.curvalue -= self.gridview.objIncr
        gSetTitle(self.valbutton, str(round(self.gridview.curvalue, 1)))
        
    def resetObjLimits(self, low, high):
        self.gridview.lowObjValue = low
        self.gridview. Value = high

    def resetObjIncr(self, incr):
        self.gridview.objIncr = incr

    def addObjectMenu (self):
        omenu = gAddMenu(self, "Objects", \
                 [["Click means Objects", self.setClickObject], \
                  ["Click means Barriers", self.setClickBarrier], \
                  ["Increment Object Value", self.incrObjValue], \
                  ["Decrement Object Value", self.decrObjValue], \
                  '---'] )
        gAddMenu(omenu, "Set object value range", \
             [["Object values -1.0 to 1.0", lambda: self.resetObjLimits(-1.0, 1.0)], \
              ["Object values -10.0 to 10.0", lambda: self.resetObjLimits(-10.0, 10.0)], \
              ["Object values -100.0 to 100.0", lambda: self.resetObjLimits(-100.0, 100.0)] ] )
        gAddMenu(omenu, "Set object value increment", \
             [["Increment/Decrement by 0.1", lambda: self.resetObjIncr(0.1)], \
              ["Increment/Decrement by 1.0", lambda: self.resetObjIncr(1.0)], \
              ["Increment/Decrement by 10.0", lambda: self.resetObjIncr(10.0)] ] )

###

def makeObjectGridworldSimulation(w=16, h=16, st=0, g=1, size=30, agentclass=DynaGridAgent):
    s = ObjectGridworldWindow(width=w, height=h, startsquare=st, goalsquare=g, squaresize=size)
    env = s.gridview
    agent = agentclass(numstates=env.numsquares, numactions=env.numactions())
    simInit(s, agent, env, False)
    return s

