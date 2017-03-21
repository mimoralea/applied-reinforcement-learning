### Routines for demonstrating 1D function learning programs.

from RLtoolkit.G.g import *
from RLtoolkit.Quickgraph.graph import *
from math import *
from .fa import *
from .tilecoder import *

window = None
black = gColorBlack(True)
flip = gColorFlip(True)
gray = gColorLightGray(True)
white = gColorWhite(True)
xresolution = 60                  # number of points across
lines = [[]]                      # the set of lines to draw when refreshing
oldlines = [[]]                   # the set of lines to draw when refreshing
showoldlines = gIntVar()          # indicates whether to show old lines, set by menu button
showoldlines.set(0)
menuloaded = False
functionapproximator = None
examples = []                     # a list of all the examples learned so far

class FADataview (Dataview):

    def gDrawView (self):
        self.parentgraph.gDrawView()
        pass

    def gClickEventHandler(self, x, y):
        self.newExample(x, y)

    def newExample (self, xarg, farg):
        global inputarray, functionapproximator, examples
        self.parentgraph.drawExample(xarg, farg, 1)
        inputarray[0] = xarg
        examples.append([xarg, farg])
        functionapproximator.faLearn(inputarray, farg)
        self.parentgraph.updateLines()
        gClear(self)
        self.parentgraph.maybeDrawOldlines()
        self.parentgraph.drawLines()
        self.parentgraph.drawEgs()

        
class DemoWindow (Graph):

    def __init__(self, title, fa, dataviewtype=FADataview, **kwargs):
        global functionapproximator
        Graph.__init__(self, title, dataviewtype, **kwargs)
        self.dataview.parentgraph = self
        xGraphLimits(0, 1, "Function Approximation Demonstration")
        yGraphLimits(-20, 36, "Function Approximation Demonstration")
        xTickmarks([0, .2, .4, .6, .8, 1],"Function Approximation Demonstration")
        yTickmarks([-20, -10, 0, 10, 20, 30],"Function Approximation Demonstration")
        self.boxy = True
        if fa == None:
            fa = makeTileCoder([[0, 1.2, 6]])
        functionapproximator = fa
        self.initDemo()
        self.setupFAdemoMenu()
    
    def gDrawView (self):
        gClear(self)
        self.drawAxes()
        self.drawEgs()
        self.maybeDrawOldlines()
        self.drawLines()
        self.message("Next Point?")

    def gDestroy(self, event):
        Gwindow.gDestroy(self, event)
        self.quit()

    def message (self, string, color1='white',color2='black'):
        "Updates the message in lower left corner"
        global black, white
        gFillRectR(self, 0, 0, \
                   gTextWidth(self, "aaaaaaaaaaaaaaaaaa", self.charstyle), \
                   gTextHeight(self, "A", self.charstyle), white)
        gDrawText(self, string, self.charstyle, 1, 4, black)

    def initDemo(self):
        global functionapproximator, lines, oldlines, examples, inputarray
        functionapproximator.faInit()
        gClear(self)
        gClear(self.dataview)
        inputarray = [0 for i in range(functionapproximator.numinputs)]
        lines = [[]]
        oldlines = [[]]
        examples = []
        self.updateLines()
        self.gDrawView()

    def reDraw(self):
        self.viewDrawContents()

    def setResolutionHigher(self):
        global xresolution
        xresolution = int(round(1.5 * xresolution))
        print("New xresolution is", str(xresolution))
        self.updateLines()
        self.reDraw()

    def setResolutionLower(self):
        global xresolution
        xresolution = int(round(0.666667 * xresolution))
        print("New xresolution is", str(xresolution))
        self.updateLines()
        self.reDraw()

    def setAlpha(self, new=0.1):
        global functionapproximator
        print("Setting alpha to", new)
        functionapproximator.setLearningrate(new)

    def setTilings(self, num = 8):
        global functionapproximator
        print("Set number of tilings to ", num)
        functionapproximator = makeTileCoder([[0, 1.2, 6]], 1, num)
        self.initDemo()

    def quitFA(self):
        self.gCloseView()
        gQuit()

    def setupFAdemoMenu (self):
        global showoldlines
        gAddMenu(self, "FA Demo", \
                [["Init", self.initDemo], \
                 ['button', "Show Old Line", showoldlines, 1, 0, None], \
                 ["Resolution Higher", self.setResolutionHigher], \
                 ["Resolution Lower", self.setResolutionLower], \
                 '---', \
                 ["Alpha = 1.0", lambda: self.setAlpha(1.0)], \
                 ["Alpha = 0.5", lambda: self.setAlpha(0.5)], \
                 ["Alpha = 0.25", lambda: self.setAlpha(0.25)], \
                 ["Alpha = 0.1", lambda: self.setAlpha(0.1)], \
                 '---', \
                 ["Number of tilings = 1", lambda: self.setTilings(1)], \
                 ["Number of tilings = 2", lambda: self.setTilings(2)], \
                 ["Number of tilings = 8", lambda: self.setTilings(8)], \
                 ["Number of tilings = 64", lambda: self.setTilings(64)], \
                 '---', \
                 ['Quit', self.quitFA]])

    def drawExample (self, x, f, intensity):
        global black
        gdDrawCircle(self.dataview, gdCoordx(self.dataview, x), gdCoordy(self.dataview, f), \
                     ceil(5 * intensity), black)

    def maybeDrawOldlines (self):
        global oldlines, gray, showoldlines
        if showoldlines.get() == 1:
            self.drawLines(oldlines, gray)

    def drawLines (self, dlines=None, color=black):
        global lines
        if dlines ==None:
            dlines = lines
        drawXY(self, dlines[0], color)

    def updateLines (self):
        global lines, oldlines, xresolution, inputarray, functionapproximator
        oldlines = lines
        nlines = []
        for i in range(xresolution):
            x = float(i) / xresolution
            fline = [x, functionapproximator.faApproximate([x])]
            nlines.append(fline)
        nlines.append(fline)    # repeat last point so last section draws
        lines = [nlines]  

    def drawEgs(self):
        global examples
        if examples != []:
            printegs = examples[:]
            printegs.reverse()
            age = 0
            for x, f in printegs:
                self.drawExample(x, f, .95**age)
                age +=1
            
def setupFAdemo (fa=None):
    global GDEVICE, \
           functionapproximator
    if fa == None:
        fa = makeTileCoder([[0, 1.2, 6]])
    functionapproximator = fa
    window = DemoWindow("Function Approximation Demonstration", fa, \
                 dataviewtype=FADataview, \
                 gdViewportR=(10,30, GDEVICE.wwidth-50, GDEVICE.wheight-50))
    
def faDemo():
    setupFAdemo(None)
    gMainloop()

if __name__ == "__main__":
    faDemo()
