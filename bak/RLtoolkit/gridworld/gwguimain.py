""" Gridworld GUI code
This file implements the GUI interface for a gridworld, using the simulation
object set up in the file guiwindow. The code is intended to be easily added to
or modified to customize for particular users or gridworld types.

The class GridworldView is the GUI view of the gridworld. This class can be
inherited and modified quite easily to display different aspects of a gridworld.
The following methods can be redefined to customize the interface:
   squareColor - chooses the color the square will be drawn with. Currently
     barriers are drawn as blue, and the value function is used for the others
   squareDrawColor - draws the color on the square
   squareDrawMore - a hook for you to draw your own stuff between the square
     coloring and the drawing of walls and arrows
   squareDrawWalls - draws the walls of the gridworld
   squareDrawArrows - draws arrows on the gridworld (currently using action values)
and for even more control, you can redefine:
   squareDrawContents
If you want to add your own controls for some events, you can redefine/modify:
   handleSquareClick - what to do if user clicks in a square

The class GridworldWindow is a specialized version of the SimulationWindow defined
in the file guiwindow. It adds menus and buttons specific to the gridworld
application. 
"""

from RLtoolkit.g import *
from RLtoolkit.guiwindow import *
from .gwAgent import *
from .gwAgent import *
from .gwSim import *
from .gwio import *
import operator

if sys.platform in ['mac', 'darwin']:
    walldiff = 3
else:
    walldiff = 3
    
class GridworldView (Gridworld, Gview):

    def __init__(self, parent, width=None, height=None, \
                 startsquare=None, goalsquare=None, squaresize=60):
        Gridworld.__init__(self, width, height, startsquare, goalsquare)
        Gview.__init__(self, parent, windowTitle="Gridworld Window")
        if squaresize == None:
            squaresize = 60
        self.squaresize = squaresize
        self.minh = self.minv = 0
        self.update = True
        self.agentblock = None
        self.arrowdisplay = True
        self.colorsdisplay = True
        self.arrowcolor = gBlack
        self.maxarrowsize = 1
        self.wallpieces = []
        self.lastselectedx = None
        self.lastselectedy = None
        self.curevent = None
        self.contents = [[] for i in range(self.numsquares)]
        gdSetViewportR(self, 0, 0, self.width*self.squaresize, \
                       self.height*self.squaresize)
        self.startandgoalfont = ("Helvetica", squaresize // 2, "bold")
        self.colors = [0 for i in range(511)]
        for c in range(256):
            pos = 255 + c
            neg = 255 - c
            self.colors[pos] = gColorRGB255(self, 255-c, 255, 255-c)
            self.colors[neg] = gColorRGB255(self, 255, 255-c, 255-c)
        self.wallDisplay()

    def gdClickEventHandler (self, dh, dv):     # GridworldView environment
        if self.dhdvInGridworldview(dh, dv):
            self.handleEventInEnvironment(dh, dv, self.sim)
 
    def handleEventInEnvironment (self, dh, dv, sim):
        agent = sim.agent
        square = self.squarefromdhdv(int(dh), int(dv))
        size = self.squaresize
        relativeh = dh - self.squaredh(square)
        relativev = dv - self.squaredv(square)
        scaledrelativeh = float(relativeh) / size
        scaledrelativev = float(relativev) / size
        centerselectedp = (scaledrelativeh > .15) and \
                          (scaledrelativeh < .85) and \
                          (scaledrelativev > .15) and \
                          (scaledrelativev < .85)
        if relativeh < 4:
            action = 3  # left
        elif relativev < 4:
            action = 0  # up
        elif relativeh > (size - 4):
            action = 1  # right
        elif relativev > (size - 4):
            action = 2  # down
        else:
             action = None

        if action != None:
            self.toggleWall(square, action)
            self.squareDrawContents(agent, square)
        if centerselectedp:
            self.lastselectedx, self.lastselectedy = dh, dv
            if square == self.state:                    # moving agent
                self.curevent = 'moveAgent'
            elif square == self.startsquare:            # moving start
                self.curevent = 'moveStart'
            elif square == self.goalsquare:             # moving goal
                self.curevent = 'moveGoal'
            else:
                self.handleSquareClick(agent, square)

    def handleSquareClick(self, agent, square):
        # toggle barrier status of square
        self.toggleBarrier(square)
        self.squareDrawContents(agent, square)
                
    def gdMouseUpEventHandler(self, dh, dv):               # finish event started
        dh, dv = int(dh), int(dv)
        agent = self.sim.agent
        if dh == self.lastselectedx and dv == self.lastselectedy:   # do nothing; already handled
            pass
        elif self.curevent == 'moveAgent':
            square = self.squarefromdhdv(dh, dv)
            self.setState(square)
            agent.agentStartEpisode(self.state)
        elif self.curevent == 'moveStart':
            square = self.squarefromdhdv(dh, dv)
            self.resetStartSquare(agent, square)
        elif self.curevent == 'moveGoal':
            square = self.squarefromdhdv(dh, dv)
            self.resetGoalSquare(agent, square)
        self.lastselectedx = None
        self.lastselectedy = None
        self.curevent = None

    def gdMotionEventHandler(self,dx,dy):
        """Do the update at each motion event so that user can see the
        item being dragged"""
        dx,dy = int(dx),int(dy)
        if self.curevent == 'moveAgent':
            square = self.squarefromdhdv(dx, dy)
            self.setState(square)
        elif self.curevent == 'moveGoal':
            agent = self.sim.agent
            square = self.squarefromdhdv(dx, dy)
            self.resetGoalSquare(agent, square)
        elif self.curevent == 'moveStart':
            agent = self.sim.agent
            square = self.squarefromdhdv(dx, dy)
            self.resetStartSquare(agent, square)

    def setColorsDisplay(self, newdisplayp):
        self.colorsdisplay = newdisplayp
        self.wholeSimDisplay()

    def squareDrawColor (self, agent, square):
        if self.contents[square] != [] and self.contents[square] != None:
            gDelete(self, self.contents[square])
            self.contents[square] = []
        if self.barrierp[square]:
            color = gBlue
        else:
            color = self.squareColor(agent, square)
        self.contents[square].append(self.gFillSquare(square, color))

    def squareDrawMore(self, agent, square):
        pass

    def squareDrawStartGoal(self, agent, square):
        if square == self.startsquare:
            self.contents[square].append(self.drawLetterAtSquare(square, "S"))
        elif square == self.goalsquare:
            self.contents[square].append(self.drawLetterAtSquare(square, "G"))

    def squareDrawWalls(self, agent, square):
        for a in range(4):
            if self.wallp[square][a]:
                self.contents[square].append(self.drawWall(square, a))

    def squareDrawArrows(self, agent, square):
        avals = agent.actionvalues(square)
        for a in range(agent.numactions):
            value = avals[a]
            self.contents[square].append(self.drawSquareLine(square, a, value))
        bestaction, bestvalue = argmaxspecial(avals)
        if bestaction != None:
            self.contents[square].append(self.drawSquareArrowhead(square, bestaction, bestvalue))

    def squareDrawContents (self, agent, square):
        # figure out better way to see what changes - dont redraw all
        if self.update:
            self.squareDrawColor(agent, square)
            self.squareDrawMore(agent, square)
            self.squareDrawStartGoal(agent, square)
            if self.barrierp[square]:
                pass
            else:   # draw walls and arrows
                self.squareDrawWalls(agent, square)
                if not (square == self.goalsquare): # or square == self.startsquare):
                    if self.arrowdisplay:
                        self.squareDrawArrows(agent, square)
                        
    def wallDisplay (self):
        "displays exterior walls"
        maxx = self.squaresize * self.width
        maxy = self.squaresize * self.height
        gDelete(self, self.wallpieces)
        self.wallpieces = []
        for x in range(0, maxx, self.squaresize):
            self.wallpieces.append(gdDrawLine(self, x, 0, x, maxy, gGray))
        for y in range(0, maxy, self.squaresize):
            self.wallpieces.append(gdDrawLine(self, 0, y, maxx, y, gGray))

    def squareColor (self, agent, square):
        "square color is based on state value"
        if not self.colorsdisplay:
            i = 255
        elif square == self.goalsquare:
            i = 510
        else:
            i = 255 + int(minmax(agent.statevalue(square), -1, 1) * 255)
        return self.colors[i]

    def drawWall (self, square, action):
        h = self.squaredh(square)
        v = self.squaredv(square)
        size = self.squaresize
        color = gBlue
        if action == 0:
            return gdDrawLineR(self, h+1, v+1, size-2, 0, color)
        elif action == 1:
            return gdDrawLineR(self, h+size-1, v+1, 0, size-2, color)
        elif action == 2:
            return gdDrawLineR(self, h+1, v+size-1, size-2, 0, color)
        elif action == 3:
            return gdDrawLineR(self, h+1, v+1, 0, size-2, color)

    def setState(self, newstate):
        self.state = newstate
        if self.update:
            if newstate != None:
                self.flipStateDisplay(newstate)

    def flipStateDisplay (self, square):
        if self.agentblock != None:
            gDelete(self, self.agentblock)
        if square == 'terminal':
            square = self.goalsquare
        self.agentblock = gdFillRectR(self, \
                        (self.squaresize // 4) + self.squaredh(square), \
                        (self.squaresize // 4) + self.squaredv(square), \
                        self.squaresize // 2, self.squaresize // 2, gOn)

    def gFillSquare (self, square, color):
        global walldiff
        return gdFillRectR(self, self.squaredh(square)+1, self.squaredv(square)+1, \
                    self.squaresize-walldiff, self.squaresize-walldiff, color) # 3 instead of 2 for non mac
       
    def resetStartSquare (self, agent, newstartsquare):
        oldstart = self.startsquare
        self.startsquare = newstartsquare
        self.squareDrawContents(agent, oldstart)
        self.squareDrawContents(agent, newstartsquare)

    def resetGoalSquare (self, agent, newgoalsquare):
        oldgoal = self.goalsquare
        self.goalsquare = newgoalsquare
        self.squareDrawContents(agent, oldgoal)
        self.squareDrawContents(agent, newgoalsquare)

    def addGWObject (self, agent, square, value):
        addObject(self, square, value)
        self.squareDrawContents(agent, square)

    def drawLetterAtSquare (self, square, letterstring):
        if square != None:
            return gdDrawTextCentered(self, letterstring, self.startandgoalfont, \
                       (self.squaresize // 2) + self.squaredh(square), \
                       (self.squaresize // 2) + self.squaredv(square), gBlack)
    ### ARROWS

    def drawSquareArrow (self, square, action):
        x = self.squaredh(square) + self.squaresize // 2
        y = self.squaredv(square) + self.squaresize // 2
        length = self.squaresize // 3
        if action == 0:
            return gdDrawArrow(self, x, y, x, y-length, self.arrowcolor)
        elif action == 1:
            return gdDrawArrow(self, x, y, x+length, y, self.arrowcolor)
        elif action == 2:
            return gdDrawArrow(self, x, y, x, y+length, self.arrowcolor)
        elif action == 3:
            return gdDrawArrow(self, x, y, x-length, y, self.arrowcolor)
     
    def setArrowDisplay(self, newdisplayp):
        self.arrowdisplay = newdisplayp
        self.wholeSimDisplay()

    def drawSquareLine (self, square, direction, length):
        halfsquaresize = self.squaresize // 2
        x = self.squaredh(square) + halfsquaresize
        y = self.squaredv(square) + halfsquaresize
        if length < 0:
            length = 0
        length = int(min(1, float(length) / self.maxarrowsize) * halfsquaresize)
        if direction == 0:
            return gdDrawLine(self, x, y, x, y-length, self.arrowcolor)
        elif direction == 1:
            return gdDrawLine(self, x, y, x+length, y, self.arrowcolor)
        elif direction == 2:
            return gdDrawLine(self, x, y, x, y+length, self.arrowcolor)
        elif direction == 3:
            return gdDrawLine(self, x, y, x-length, y, self.arrowcolor)

    def drawSquareArrowhead (self, square, direction, length):
        halfsquaresize = self.squaresize // 2
        x = self.squaredh(square) + halfsquaresize
        y = self.squaredv(square) + halfsquaresize
        if length < 0:
            direction = direction + 2 // 4  #opposite direction
        length = int(min(1, float(length) / self.maxarrowsize) * halfsquaresize)
        if direction == 0:
            return gdDrawArrowhead(self, x, y, x, y-length, 0, 0.25, self.arrowcolor)
        elif direction == 1:
            return gdDrawArrowhead(self, x, y, x+length, y, 0, 0.25, self.arrowcolor)
        elif direction == 2:
            return gdDrawArrowhead(self, x, y, x, y+length, 0, 0.25, self.arrowcolor)
        elif direction == 3:
            return gdDrawArrowhead(self, x, y, x-length, y, 0, 0.25, self.arrowcolor)

    def setMaxArrowSize(gw, newmaxsize):
        gw.maxarrowsize = newmaxsize
        gw.viewDrawContents()  #gdDrawView

    ### Gridworld utilities
        
    def inverseaction (self, action):
        return action + 2 % 4

    def squaredv (self, square):
        return self.minv + (self.squaresize * self.squarev(square))

    def squaredh (self, square):
        return self.minh + (self.squaresize * self.squareh(square))

    def dhdvInGridworldview (self, dh, dv):
        return (dh >= self.minh) and (dv >= self.minv) and \
               (dh <= (self.minh + (self.squaresize * self.width))) and \
               (dv <= (self.minv + (self.squaresize * self.height)))

    def squarefromdhdv (self, dh, dv):
        return self.squarefromhv(max(0, min(self.width-1, (dh-self.minh) // self.squaresize)), \
                    max(0, min(self.height-1, (dv-self.minv) // self.squaresize)))

class GridworldWindow (SimulationWindow):

    def __init__(self, width=None, height=None, startsquare=None, goalsquare=None, \
                 squaresize=None, gridtype=GridworldView):
        wwidth = width * squaresize
        wheight = height * squaresize
        SimulationWindow.__init__(self, wwidth, wheight)
        self.gridview = gridtype(self, width, height, startsquare, goalsquare, squaresize)
        x1, y1, x2, y2 = gdGetViewport(self)        # get viewport info
        gdSetViewport(self, x1, y1, x2, y2+30)   # add enough for buttons
        gdAddButton(self, "DP Values", self.simAvi, 5, self.wheight - 30)  
        gdAddButton(self, "Value It", self.simVI1, 100, self.wheight - 30) 
        self.showpolicyarrows = gIntVar()
        self.showpolicyarrows.set(1)
        self.showvaluecolors = gIntVar()
        self.showvaluecolors.set(1)
        self.addGridworldMenu()
        self.addAgentMenu()
        self.addModelMenu()
        self.readtitle = "Choose Gridworld to Open"
        self.writetitle = "Save Current Gridworld As"
        self.initialdir = gwPath()

    def simAvi(self):
        if not isinstance(self.agent, DynaGridAgent):
            print("Cannot do DP on non model agent")
        else:   
            avi(self)
            self.wholeSimDisplay()

    def simVI1(self):
        if not isinstance(self.agent, DynaGridAgent):
            print("Cannot do Value Iteration on non model agent")
        else:
            vi1(self)
            self.wholeSimDisplay()

    def updateSimDisplay(self):
        agent = self.agent
        if agent != None:
            if self.episodestepnum == 0:
                self.display(list(range(agent.numstates)))
            else:
                self.display(agent.changedstates)

    def display(self, displaystates):
        agent = self.agent
        gwv = self.env
        oldupdate = gwv.update
        gwv.update = True
        for square in displaystates:
            gwv.squareDrawContents(agent, square)
        agent.changedstates = []
        #draw current agent location
        if gwv.state != None:
            gwv.flipStateDisplay(gwv.state)
        else:
            gwv.flipStateDisplay(gwv.startsquare)
        gwv.update = oldupdate

    def wholeSimDisplay(self):
        self.env.wallDisplay()
        agent = self.agent
        if agent != None:
            self.display(list(range(agent.numstates)))

    # Opening and writing gridworld files

    def readFile(self, filename):
        if filename != None and filename != '':       
            list = readGridworld(filename)
            gridworld = self.genGridworld(list)
            setWindowTitleFromNamestring(gridworld, filename)

    def writeFile(self, filename):
        olist = prepareWrite(self.gridview)
        writeGridworld(olist, filename)

    def genGridworld(self, alist, agentclass=DynaGridAgent):
        width, height, startsquare, goalsquare, barrierp, wallp = getgwinfo(alist)
        squaresize = alist.get('squaresize')
        gridworld = GridworldWindow (width, height, startsquare, goalsquare, squaresize)
        gview = gridworld.gridview
        if barrierp != None:
            gview.barrierp = barrierp
        if wallp != None:
            gview.wallp = wallp
        gview.updatedisplay = True
        agent = agentclass(numstates=gview.numsquares, numactions=gview.numactions())
        simInit(gridworld, agent, gview, False)
        return gridworld

    def resetSimulation(self):
        resetSim(self)
        self.wholeSimDisplay()

    def makeNewSimulation(self, w=16, h=16, st=0, g=1, size=30, agentclass=DynaGridAgent):
        s = GridworldWindow(width=w, height=h, startsquare=st, goalsquare=g, squaresize=size)
        env = s.gridview
        agent = agentclass(numstates=env.numsquares, numactions=env.numactions())
        simInit(s, agent, env, False)
        return s

    # Agent stuff

    def changeagent (self, new):
        changeAgentLearnMethod(self, new)
        simInit(self, self.agent, self.env, False)
        resetSim(self)
        self.wholeSimDisplay()
        
    def resetpar (self, name, value):
        eval('resetParameters(self.agent,' + name + '=' + str(value) + ')')
        
    def displayPars (self):
        displayParameters(self.agent)

    def initActionValues (self):
        saveQ(self.agent)
        for s in range(self.env.numstates()):
            for a in range(self.env.numactions()):
                self.agent.Q[s][a] = self.agent.initialvalue
        self.wholeSimDisplay()

    def revertValues (self):
        restoreQ(self.agent)
        self.wholeSimDisplay()

    def addAgentMenu(self):
        amenu = gAddMenu(self, "Agent", \
             [["New agent with One step Q learning", lambda: self.changeagent("onestepq")], \
              ["New agent with Q(lambda)", lambda: self.changeagent("qlambdareplace")], \
              ["New agent with Sarsa learning", lambda: self.changeagent("sarsa")], \
              ["New agent with Sarsa(lambda)", lambda: self.changeagent("sarsalambdatraces")], \
              ["New agent with One step dyna", lambda: self.changeagent("onestepdyna")],\
              '---', \
              ["Init Values", self.initActionValues], \
              ["Revert Values", self.revertValues], \
              '---', \
              ["Display Agent Parameters", lambda: self.displayPars()], \
              '---'] )
        gAddMenu(amenu, "Change epsilon", \
             [["Set epsilon = 0.0", lambda : self.resetpar('epsilon', 0.0)], \
              ["Set epsilon = 0.01", lambda: self.resetpar('epsilon', 0.01)], \
              ["Set epsilon = 0.05", lambda: self.resetpar('epsilon', 0.05)], \
              ["Set epsilon = 0.1", lambda: self.resetpar('epsilon', 0.1)], \
              ["Set epsilon = 0.5", lambda: self.resetpar('epsilon', 0.5)], \
              ["Set epsilon = 1.0", lambda: self.resetpar('epsilon', 1.0)] ])
        gAddMenu(amenu, "Change alpha", \
             [["Set alpha = 0.0", lambda: self.resetpar('alpha', 0.0)], \
              ["Set alpha = 0.1", lambda: self.resetpar('alpha', 0.1)], \
              ["Set alpha = 0.25", lambda: self.resetpar('alpha', 0.25)], \
              ["Set alpha = 0.5", lambda: self.resetpar('alpha', 0.5)], \
              ["Set alpha = 0.9", lambda: self.resetpar('alpha', 0.9)], \
              ["Set alpha = 1.0", lambda: self.resetpar('alpha', 1.0)] ] )
        gAddMenu(amenu, "Change gamma", \
             [["Set gamma = 0.0", lambda: self.resetpar('gamma', 0.0)], \
              ["Set gamma = 0.1", lambda: self.resetpar('gamma', 0.1)], \
              ["Set gamma = 0.5", lambda: self.resetpar('gamma', 0.5)], \
              ["Set gamma = 0.9", lambda: self.resetpar('gamma', 0.9)], \
              ["Set gamma = 1.0", lambda: self.resetpar('gamma', 1.0)] ] )
        gAddMenu(amenu, "Change lambda", \
             [["Set lambda = 0.0", lambda: self.resetpar('agentlambda', 0.0)], \
              ["Set lambda = 0.5", lambda: self.resetpar('agentlambda', 0.5)], \
              ["Set lambda = 0.8", lambda: self.resetpar('agentlambda', 0.8)], \
              ["Set lambda = 1.0", lambda: self.resetpar('agentlambda', 1.0)] ] )
        gAddMenu(amenu, "Change exploration bonus", \
             [["Set expl bonus = 0.0", lambda: self.resetpar('explorationbonus', 0.0)], \
              ["Set expl bonus = 0.0001", lambda: self.resetpar('explorationbonus', 0.0001)], \
              ["Set expl bonus = 0.001", lambda: self.resetpar('explorationbonus', 0.001)], \
              ["Set expl bonus = 0.01", lambda: self.resetpar('explorationbonus', 0.01)] ] )
        gAddMenu(amenu, "Change initial value", \
             [["Set initial value = -0.1", lambda: self.resetpar('initialvalue', -0.1)], \
              ["Set initial value = 0.0", lambda: self.resetpar('initialvalue', 0.0)], \
              ["Set initial value = 0.01", lambda: self.resetpar('initialvalue', 0.01)], \
              ["Set initial value = 0.1", lambda: self.resetpar('initialvalue', 0.1)], \
              ["Set initial value = 0.5", lambda: self.resetpar('initialvalue', 0.5)], \
              ["Set initial value = 1.0", lambda: self.resetpar('initialvalue', 1.0)] ] )

    def toggleShowArrows (self):
        self.gridview.arrowdisplay = not self.gridview.arrowdisplay
        self.wholeSimDisplay()
        
    def toggleShowColors (self):
        self.gridview.colorsdisplay = not self.gridview.colorsdisplay
        self.wholeSimDisplay()

    # model stuff
    
    def correctModel (self):
        setupAccurateModel(self)
        avi(self)
        self.wholeSimDisplay()
        
    def emptyModel (self):
        setupNullModel(self)
        avi(self)
        self.wholeSimDisplay()
        
    def setModelNoObstacles (self):
        setupEmptyGridModel(self)
        avi(self)
        self.wholeSimDisplay()
        
    def setModelStay (self):
        setupStayModel(self.agent)
        avi(self)
        self.wholeSimDisplay()
         
    def revealGoal (self):
        revealGoalLocation(self)
        self.wholeSimDisplay()

    def revertModel (self):
        restoreModel(self.agent)
        self.wholeSimDisplay()

    def addGridworldMenu (self):
        m = gAddMenu(self, "Gridworld", \
                 [
                  ['button', "Show Policy Arrows", self.showpolicyarrows, 1, 0, \
                   lambda: self.toggleShowArrows()], \
                  ['button', "Show Value Colors", self.showvaluecolors, 1, 0, \
                   lambda: self.toggleShowColors()], \
                  "---", \
                  ["6 x 8 gridworld", \
                   lambda: self.readFile(gwFilename('gw8x6'))], \
                  ["16 x 10 gridworld", \
                   lambda: self.readFile(gwFilename('gw16x10'))], \
                  ["16 x 10 cleared gridworld", \
                   lambda: self.readFile(gwFilename('gw16x10cleared'))], \
                  ["16 x 16 cleared gridworld", \
                   lambda: self.readFile(gwFilename('gw16x16'))], \
                  '---' ] )
        gAddMenu(m, "New Gridworld", \
                  [["4x1", lambda: self.makeNewSimulation(4, 1, 0, 3, 80)], \
                   ["2x2", lambda: self.makeNewSimulation(2, 2, 0, 3, 160)], \
                   ["8x1", lambda: self.makeNewSimulation(8, 1, 0, 3, 80)], \
                   ["4x4", lambda: self.makeNewSimulation(4, 4, 0, 15, 160)], \
                   ["8x6", lambda: self.makeNewSimulation(8, 6, 0, 47, 70)], \
                   ["6x8", lambda: self.makeNewSimulation(6, 8, 0, 47, 70)], \
                   ["8x8", lambda: self.makeNewSimulation(8, 8, 0, 47, 70)], \
                   ["10x10", lambda: self.makeNewSimulation(10, 10, 0, 99, 60)], \
                   ["10x16", lambda: self.makeNewSimulation(10, 16, 0, 159, 40)], \
                   ["16x10", lambda: self.makeNewSimulation(16, 10, 0, 159, 60)], \
                   ["16x16", lambda: self.makeNewSimulation(16, 16, 0, 255, 40)], \
                   ["20x20", lambda: self.makeNewSimulation(20, 20, 0, 399, 30)], \
                   ["40x40", lambda: self.makeNewSimulation(40, 40, 0, 1599, 20)] ] )
                                                                                 
    def addModelMenu (self):
        gAddMenu(self, "Model", \
                 [["DP Values", self.simAvi], \
                  ["Value Iteration", self.simVI1], \
                  '---', \
                  ["Correct Model", lambda: self.correctModel()], \
                  ["Empty Model", lambda: self.emptyModel()], \
                  ["No Obstacles Model", lambda: self.setModelNoObstacles()], \
                  ["Stay Model", lambda: self.setModelStay()], \
                  ["Reveal Goal", lambda: self.revealGoal()], \
                  '---', \
                  ["Revert Model", lambda: self.revertModel()] ] )



###

def makeGridworldSimulation(w=16, h=16, st=0, g=1, size=30, \
                            gridworldclass=GridworldWindow, agentclass=DynaGridAgent):
    s = gridworldclass(width=w, height=h, startsquare=st, goalsquare=g, squaresize=size)
    env = s.gridview
    agent = agentclass(numstates=env.numsquares, numactions=env.numactions())
    simInit(s, agent, env, False)
    return s


