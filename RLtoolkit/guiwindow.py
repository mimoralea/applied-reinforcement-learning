"""
This file implements a general simulation interface. The SimulationWindow has a space
for thedisplay of a specific task, a display area showing the counts of steps and
episodes so far, and buttons for controlling the simulation. It also adds two menus -
a File menu and a Simulation menu.
It is easy to make a GUI simulation interface for your RL task by specializing
the SimulationWindow class with methods appropriate for your application.

Make a specialized simulation window class with:
class MyApplication(SimulationWindow):
    def __init__(wwidth, wheight): # wwidth and wheight specify the size of the data display area you want.
        SimulationWindow.__init__(self, wwidth, wheight)
        ... your own stuff here ...
        ... including setting various members and adding extra buttons and menus
        Make gViews with the SimulationWindow as the parent for the data areas in your simulation interface.

        It uses an RLinterface to do the actual steps and episodes. In your initialization, make
        sure that you set the data member rlsim to an RLinterface.
        self.rlsim = RLinterface(agentFunction, EnvironmentFunction)

The following methods can and in some cases should be defined by the user:
   updateSimDisplay(self) - update the data display area of the simulation - required!
   wholeSimDisplay(self)  - redraw the data display area of the simulation - required!
   printInfo(self) - what to do if the user chooses Print under the File menu
   resetSimulation(self) - resets the agent and environment
   
For reading and writing, define methods:
   readFile(self, filename) - reads filename
       (called from openFile, invoked by Open on File menu)
   writeFile(self, filename) - writes current simulation info into filename
       (called from saveFile and saveFileAs, invoked by Save and SaveAs on File menu)
also set self.readtitle as the title of the open file dialog
            self.writetitle as the title of the save file dialog
            self.initialdir as the directory to start reading or writing at
or for more control, specify the menu handling methods themselves:  
   openFile(self) - what to do if the user chooses Open under the File menu
   saveFile(self) - what to do if the user chooses Save under the File menu
   saveFileAs(self) - what to do if the user chooses Save As under the File menu
   
The preset buttons are:
   Start/Stop - starts or stops a currently running simulation
   Step - executes one step of the simulation 
   Episode - executes one episode of the simulation
     The previous 3 buttons use the RLinterface member and call methods step and episode for it
   Faster - makes the execution faster by updating the display less
   Slower - makes the execution slower by updating the display more or pausing before updates

Menu items:
   File menu:
      Open     - calls method openFile(self)
      Save     - calls method saveFile(self)
      Save As  - calls method saveFileAs(self)
      Print    - calls method printInfo(self)
      Quit     - quits the simulation and stops event processing
   Simulation menu:  the button commands are repeated here, and some additional things
      Start/Stop simulation
      Step simulation
      Simulate one episode
      Faster
      Slower
      Redisplay  - calls method gDrawView
      Redisplay All - calls method wholeView
      Reset Simulation   - calls method resetSimulation(self)

Some methods which you may wish to call:
   gDrawView(self) - force updating of the whole display
   wholeView(self) - force redrawing of the whole display
   debugon(self) - returns True is debug mode is set to on, False otherwise

Note: your agent and environment functions should update the data members
   stepnum, episodenum, and episodestepnum for the count displays to work properly
"""

# Example of usage:
"""
Given functions myAgentFn and myEnvFn that conform to the RLinterface requirements:

def myAgentFn(state, reward=None):
   ...
   return action

def myEnvFn(action=None):
   ...
   ... increment stepnum, episodestepnum, episodenum appropriately
   return state, reward

class MySimClass (SimulationWindow):
   def __init__(self, wwidth, wheight):
      SimulationWindow.__init__(wwidth, wheight)
      gSetTitle(self, "My Simulation")
      self.rlsim = RLinterface(myAgentFn, myEnvFn)
      dataview = Gview(self)
      ...draw desired stuff on the dataview ...

    def wholeSimDisplay(self):
      ...draw dataview however you want...
      gMakeVisible(self)  # might be necessary to force the changes to show

    def updateSimDisplay(self):
      ... update dataview with current data ...
      gMakeVisible(self)    # might be necessary to force the changes to show

    def resetSimulation(self):
       ... reset agent info ...
       ... reset environment inf, including stepnum, episodestepnum and episodenum
       self.wholeView()    # force drawing of entire simulation display

mysim = MySimClass(1000, 1000)
gMainloop()


To add additional buttons or menus:
   inside __init__
       x1, y1, x2, y2 = gdGetViewport(self)
       gdSetViewport(self, x1, y1+20, x2, y2+50)   # compensate for title bar, add enough for buttons
       gdAddButton(self, "myNewButton", self.myFunction, 5, y2)
       self.addMyMenu()              # add another menu

    def myFunction(self):
       ...
       self.wholeSimDisplay()

    def addMyMenu(self):
       gAddMenu(self, "My Menu", ...)

"""

from RLtoolkit.g import *
from RLtoolkit.basicclasses import *
import sys
import time


class SimulationWindow (Gwindow, Simulation):

    def __init__(self, wwidth=500, wheight=600):
        Simulation.__init__(self)
        if sys.platform in ['mac', 'darwin']:
            extrah = 30
        else:
            extrah = 50     # account for menu being added to window in Windows and Linus
        Gwindow.__init__(self, windowTitle="Simulation Window", gdViewportR=(0, 20, wwidth, wheight+extrah))
        self.simulationrunning = False
        self.updatedisplay = True
        self.displaypause = 0 
        self.redrawinterval = 1 
        self.countsx = self.countsy = 0         # xcoord and ycoord of time displays
        self.lastcount = None
        self.dcount = 0                         # display counter
        self.status = Gview(self)
        self.goff = gColorOff(self)
        gdSetViewportR(self.status, 0, wheight, wwidth, 30)
        self.gobutton = gdAddButton(self.status, "Go  ", self.simStopGo, 5, 0, self.goff)
        self.stepbutton = gdAddButton(self.status, "Step", self.singleStep, 65, 0, self.goff)
        self.episodebutton = gdAddButton(self.status, "Episode", self.singleEpisode,125, 0, self.goff)
        if wwidth < 350:        # make the window longer and add the buttons there
            gdSetViewportR(self.status, 0, wheight, wwidth, 60)
            self.fastbutton = gdAddButton(self.status, "Faster ", self.simFaster, 5, 30, self.goff)
            gdAddButton(self.status, "Slower", self.simSlower, 80, 30, self.goff)
        else:                   # add the buttons horizontally
            self.fastbutton = gdAddButton(self.status, "Faster ", self.simFaster, 210, 0, self.goff)
            gdAddButton(self.status, "Slower", self.simSlower, 285, 0, self.goff)
        self.debug = gIntVar()
        self.debug.set(0)
        self.setupTimeDisplay()
        self.addFileMenu()
        self.addSimulationMenu()
        self.readtitle = "Open File"
        self.writetitle = "Save File As"
        self.initialdir = None
        
    def gDrawView (self):
        if self.updatedisplay:
            self.updateSimDisplay()
        self.simDisplayCounts()
        gMakeVisible(self)

    def gKeyEventHandler(self, key):
        print("got key", key)

    def wholeView (self):
        self.dcount = 0
        self.wholeSimDisplay()
        self.simDisplayCounts()
        gMakeVisible(self)

    def simstep(self):
        if self.simulationrunning:
            self.rlsim.stepsQ(self.redrawinterval)  # do a number of steps at once for speed
            self.simDisplay()
            gCheckEvents(self, self.simstep)
            #self.after(1, self.simstep)     # using tk method after to force it to check for stop event

    def simStopGo (self):
        if self.simulationrunning:              # already running, stop it
            self.simulationrunning = False      # setSimulationRunning(self, False)
            gButtonEnable(self.stepbutton)
            gButtonEnable(self.episodebutton)
            gSetTitle(self.gobutton, "Go  ")
            self.wholeView()
        else:                                   # set it running
            self.simulationrunning = True       # setSimulationRunning(self, True)
            gButtonDisable(self.stepbutton)
            gButtonDisable(self.episodebutton)
            gSetTitle(self.gobutton, "Stop")
            gMakeVisible(self)
            self.simstep()

    def singleStep (self):
        self.rlsim.step()
        self.wholeView()

    def epstep(self):
        if self.simulationrunning:
            self.rlsim.step()                   # one step at a time - must check for episode termination
            self.simDisplay()
            if self.rlsim.action != None:       # end of episode
                gCheckEvents(self, self.epstep)
                #self.after(1, self.epstep)      # using tk method after to force it to check for stop event
            else:
                self.simStopGo()                # reset buttons on display
    
    def singleEpisode (self):
        if not self.simulationrunning:
            gButtonDisable(self.stepbutton)
            gButtonDisable(self.episodebutton)
            gSetTitle(self.gobutton, "Stop")
            self.simulationrunning = True
            self.rlsim.action = None    # force start of episode
            self.epstep()
  
    def simFaster (self):
        if self.displaypause == 0:
            gSetTitle(self.fastbutton, "Jumpier")
            self.redrawinterval = 2 * self.redrawinterval
            if self.redrawinterval > 32:
                self.updatedisplay = False
        elif self.displaypause <= 0.01:
            self.displaypause = 0
            gSetTitle(self.fastbutton, "Faster ")
            self.redrawinterval = 1
        else:
            self.displaypause = self.displaypause / 2

    def simSlower (self):
        if self.displaypause > 0:
            self.updatedisplay = True
            self.displaypause = max(0.01, 2 * self.displaypause)
        elif self.redrawinterval == 1:
            self.updatedisplay = True
            gSetTitle(self.fastbutton, "Faster ")
            self.displaypause = 0.01
        else:
            self.updatedisplay = True
            self.redrawinterval = self.redrawinterval // 2
            if self.redrawinterval == 1:
                gSetTitle(self.fastbutton, "Faster ")

    def simDisplay (self):
        self.dcount += 1
        pause(self.displaypause)
        if self.redrawinterval != None and self.dcount % self.redrawinterval == 0:
            self.gDrawView()

    def gDestroy(self, event):
        global GDEVICE
        Gwindow.gDestroy(self, event)
        if GDEVICE.childwindows == []:
            self.quit()
            
    def exit(self):
        gQuit()

    def setupTimeDisplay (self):
        oldx1, oldy1, oldx2, oldy2, oldcorner = gGetCS(self.status)
        self.countsy = 10 
        self.countsx = self.wwidth - 60 

    def simDisplayCounts (self):
        # Note: the specific application must update the stepnum, episodenum
        # and episodestepnum !!!
        if self.countsx != None:
            if self.lastcount != None:
                gDelete(self.status, self.lastcount)
            countstr = str(self.stepnum) + '|'+ str(self.episodenum) + \
                       '|'+ str(self.episodestepnum)
            self.lastcount = gdDrawTextCentered(self.status, countstr, ("Chicago", 12, "normal"), \
                                                self.countsx, self.countsy, gOn)

    def wholeSimDisplay(self):
        "display routine to redraw entire display - should be specified for each application"
        pass

    def updateSimDisplay(self):
        "update routine for display - should be specialized for each application"
        pass

    def openFile(self):
        "open simulation file"
        filename = gOpenFileUserPick(None, \
                                     title = self.readtitle, \
                                     initialdir = self.initialdir)
        self.readFile(filename)

    def readFile(self, filename):
        "open file - should be specialized for each application"
        print("File not read - there is no readFile method")
        pass

    def saveFile(self):
        "save currently open file"
        filename = filenameFromTitle(self.title)
        if filename != None and filename !="":
            self.writeFile(filename)  
        else:
            self.saveFileAs()
        pass

    def saveFileAs(self):
        "save current simulation as"
        filename = gSaveFileUserPick(self, \
                                     title = self.writetitle, \
                                     initialdir = self.initialdir)
        if filename != None and filename != '':            # not cancelled
            self.writeFile(filename)
            setWindowTitleFromNamestring(self, filename)

    def writeFile(self, filename):
        "save current simulation info - should be specialized for each application"
        print("File not saved - there is no writeFile method")
        pass

    def printInfo(self):
        "print simulation info - should be specialized for each application"
        pass

    def resetSimulation(self):
        "reset simulation - should be specialized for each application"
        pass

    def debugon(self):
        if self.debug.get() == 1:
            return True
        else:
            return False

    def toggleDebug(self):
        debugset(self.debugon())

    def addSimulationMenu(self):
        gAddMenu(self, "Simulation", \
                 [["Start/Stop simulation", self.simStopGo], \
                  ["Step simulation", self.singleStep], \
                  ["Simulate one episode", self.singleEpisode], \
                  ["Faster ", self.simFaster], \
                  ["Slower", self.simSlower], \
                  '---', \
                  ["Redisplay", self.gDrawView], \
                  ["Redisplay All", self.wholeView], \
                  '---', \
                  ["Reset Simulation", self.resetSimulation], \
                  '---', \
                  ['button', "Debug Mode", self.debug, 1, 0, self.toggleDebug], \
                  ] )
        
    def addFileMenu(self):
        gAddMenu(self, "File", \
                 [["Open ...", self.openFile], \
                  ["Save", self.saveFile], \
                  ["Save As ...", self.saveFileAs], \
                  ["Print", self.printInfo], \
                  ["Quit", self.exit] ] )
    
def pause (seconds):
    time.sleep(seconds)
    """
    x = 0
    for i in range(int(seconds * 118000000)):
        x*= 1
    """
def filenameFromTitle(title):
    position = title.find('-')
    if position != None and position != -1:
        name = title[:position]
        path = title[position+1:]
        filename = path + '/' + name
        filename = filename.strip()
        return filename
    
def setWindowTitleFromNamestring (window, filename):
    if isinstance(window, Gwindow):
        position = filename.rfind('/')
        if position == None or position == -1:
            newtitle = filename
        else:
            newtitle = filename[position+1:] + ' - ' + filename[:position]
        window.title = newtitle
        gSetTitle(window, newtitle)
