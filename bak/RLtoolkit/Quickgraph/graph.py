#   <html><head><title> Graph.py Source Code </title></head><body><pre>

"""
Source Code for graph.py, a quickgraphing tool for 
for Python.  See http://rlai.cs.ualberta.ca/RLAI/RLtoolkit/graph.html for <a href=graph.html>documentation</a>.
The function graph will draw a graph in a window, with each data line given a 
different color. 

A graph is a window with various state vars.  The simplest way to use this is:

graph(data) 
and then, possibly, graphMore(data)
you may also graphLess(color) 

or specifying the graphname,   
    graph(data, color, graph)
    graphMore(newdata, color, graph)
    graphLess(color, graph)
    
The graph involved defaults to the first graph or a newly created graph
if there are no graphs yet (or if graph is True). Alternatively, you can make 
multiple graphs, and specify the graph as a last argument to all graph routines.

Data can be a simple list of y's (heights) or a list of list of y's.
Or it can be a list of (x y) coordinates, e.g., ((x1 y1) (x2 y2) ...)
Or a list of those!

The span of the graph is initially set from the data.  Alternatively:
   xGraphLimits(xmin, xmax) does it manually (same for yGraphLimits)
   xGraphLimits() sets it back to auto

Tick marks are initially just at the min and max.  Alternatively:
   xTickmarks([tick1, tick2, tick3 ...]) sets them manually (same for yTickmarks)
   xTickmarks() sets them back to auto
   xTickmarks(num) sets them to go from the graph minimum to the maximum by num
       (call it after you make the graph to use this)
 Tick marks are specified by values, e.g., xTickmarks(0 .5, 1.0) 
 or by a list of valuelabel pairs, e.g., xTickmarks( (0, "0"), (1.0, "1"))

gridgraph(density, graph) creates a grid across the graph
graphPointsOnly(graph) makes dots on the graph for each point rather than a continuous line

histogram([val1, val2, ...], numbins, minex, maxex, color, hist)
  creates a histogram of the values. All parameters except the data list are optional
histogramMore([val1, val2, ...], numbins, minex, maxex, color, hist)
  adds another histogram graph on top of the current one

When the graph is drawn, you can highlight lines in it to see them better. The space bar
turns highlighting on and off. Highlighting will start with the first data line. Use the arrow
keys to move to the next or previous lines in the graph.

To get rid of a graph:
   closeGraph(graph) can be called with the graph or its name. If None, the first
      graph in the list of windows will be closed
"""
# if we only have the quickgraph package, use g from that. But if the whole
# toolkit is installed, use g from that

try:
    from RLtoolkit.G.g import *
except:
    from .g import *
    
import operator
import math
from functools import reduce

class Dataview (Gview):
    "dataview of graph"
    def __init__(self, parent, gdViewport):
        Gview.__init__(self, parent)
        gdSetViewport(self, gdViewport[0], gdViewport[1], gdViewport[2], gdViewport[3])
        gSetCursor(self, 'crosshair')
        
    def gClickEventHandler(self, x, y):
        print("Clicked at", x, y)
            
    def gKeyEventHandler(self, key):
        graph = self.parent
        if key == "Left" or key == "Up":
            removeHighlight(graph)
            graph.highlightline = (graph.highlightline - 1) % len(graph.data)
            drawHighlight(graph)
        elif key == "Right" or key == "Down":
            removeHighlight(graph)
            graph.highlightline = (graph.highlightline + 1) % len(graph.data)
            drawHighlight(graph)
        elif key == "space":
            removeHighlight(graph)
            graph.highlightp = not graph.highlightp
            drawHighlight(graph)
            
class Graph (Gwindow):

    def __init__(self, title="Graph", dataviewtype=Dataview, **kwargs): #(0,40,500,200)):
        self.dataview = None
        self.dviewtype = dataviewtype
        self.maincolor = gBlack
        self.data = None
        self.autolimitsx = True       # limiting x values from data, 
        self.autolimitsy = True       # or from user and tickmarks?
        self.xmax = 1.0
        self.xmin = 0.0
        self.ymax = 1.0
        self.ymin = 0.0
        self.xtickmarks = []        # initial tick marks auto from limits
        self.ytickmarks = []
        self.charstyle = gFont("Geneva", 9, 'normal')
        self.charwidth = 6
        self.charheight = 8
        self.ylabelspace = 0
        self.xlabelspace = 0
        self.zerospace = 15
        self.xendspace = 10
        self.yendspace = 10
        self.ticklength = None
        self.boxy = False
        self.pointsonly = False
        self.griddensity = None
        self.highlightp = False
        self.highlightcolor = None
        self.highlightline = 0
        self.lasthighlight = None
        if not ('gdViewport' in kwargs or 'gdViewportR' in kwargs or 'gViewport' in kwargs or 'gViewportR' in kwargs):
            Gwindow.__init__(self, windowTitle=title, gdViewport=(0,40,600,300))
        else:
            Gwindow.__init__(self, windowTitle=title, **kwargs) 
        self.initGraph()


## The data is a list of lists.  Each list is either a list of yvalues or
## a list of xypairs.

    def initGraph (self):
        self.xlabelspace = 11 * self.charwidth
        self.ylabelspace = 10 + self.charheight
        self.ticklength = self.zerospace / 2
        gSetCSScale(self, 0, 0, 1, 1, 'lowerLeft')
        x1, y1, x2, y2 = gGetViewport(self)
        self.dataview = self.dviewtype(self, gdViewport=(self.xlabelspace+1, \
                                                         self.yendspace, \
                                                         x2- self.xendspace, \
                                                         y2-self.ylabelspace-1))
        gClear(self.dataview, 'white')
        gSetCoordinateSystem(self.dataview, self.xmin, self.ymin, self.xmax, self.ymax, 'lowerLeft')
        self.maincolor = gColorOn(self.dataview) 
        self.highlightcolor = gColorPen(self.dataview, gColorFlip(self.dataview), None, None, 2, 2)
    
    def gAcceptNewViewportSize(self):
        gSetCSScale(self, 0, 0, 1, 1, 'lowerLeft')
        if isinstance(self, Graph) and self.dataview != None:
            x1, y1, x2, y2, corner = gGetCoordinateSystem(self)
            gdSetViewport(self.dataview, \
                            self.xlabelspace +1, \
                            self.yendspace, \
                            x2-self.xendspace, \
                            y2-self.ylabelspace-1)
            gClear(self.dataview, 'white')
            self.gDrawView()
    
    def gDrawView(self):
        "Draws the graph"
        gClear(self, 'white')
        gClear(self.dataview, 'white')
        self.drawAxes()
        if self.data != None:
            for color, dlist in self.data:
                drawLine(self, dlist, color)
            if self.highlightp:
                drawHighlight(self)
        if self.griddensity != None:
            gridGraph(None, self)
    
    def drawAxes (self):
        xspace = self.xlabelspace #abs(gOffsetx(self, self.xlabelspace)) 
        yspace = self.ylabelspace #abs(gOffsety(self, self.ylabelspace))
        gDrawLine(self, self.xlabelspace, yspace, \
                gConvertx(self.dataview, self, self.xmax)+self.xlabelspace, \
                yspace, \
                self.maincolor)
        gDrawLine(self, xspace, self.ylabelspace, \
                xspace, \
                gConverty(self.dataview, self, self.ymax)-self.yendspace, \
                self.maincolor)
        self.drawTickmarks()

    def drawTickmarks (self):
        xspace = self.xlabelspace #abs(gOffsetx(self, self.xlabelspace)) 
        yspace = self.ylabelspace #abs(gOffsety(self, self.ylabelspace))
        if self.xtickmarks != [] and self.xtickmarks != None:
            useticks = self.xtickmarks
        else:
            useticks = regularizeTickmarks([self.xmin, self.xmax])
        if self.xmin <= self.xmax:
            for x, label in useticks:
                gx = gConvertx(self.dataview, self, x)+self.xlabelspace
                gDrawLineR(self, gx, yspace, 0, -self.ticklength, self.maincolor)
                gDrawText(self, label, self.charstyle, \
                                gx - (self.charwidth * len(label)) /2, \
                                yspace - 5 - self.charheight, self.maincolor)
        if self.ytickmarks != [] and self.ytickmarks != None:
            useticks = self.ytickmarks
        else:
            useticks = regularizeTickmarks([self.ymin, self.ymax])
        if self.ymin <= self.ymax:
            for y, label in useticks:
                gy = gConverty(self.dataview, self, y)-self.yendspace
                gDrawLineR(self, xspace, gy, -self.ticklength, 0, self.maincolor)
                gDrawText(self, label, self.charstyle, \
                                xspace - 5 - (self.charwidth * len(label)), \
                                gy - (self.charheight / 2), self.maincolor)
        
    def gKeyEventHandler(self, key):            # send key presses to dataview handler
        self.dataview.gKeyEventHandler(key)

def removeNulls(l):
    for i in range(l.count(None)):
        l.remove(None)
    for i in range(l.count([])):
        l.remove([])
        
def graph (newdata, color=None, graph=None):     #<a name="graph"</a>[<a href="graph.html#graph">Doc</a>]
    "Establishes some data for a graph, then draws it"
    if None in newdata or [] in newdata:
        print("Warning: Some data to be graphed was nil; ignoring")
        removeNulls(newdata)
    if newdata == []:
        print("No graphing data")
    else:
        graph = chooseGraph(graph)
        graph.data = FillInColors (regularizeData(newdata, color))
        graph.highlightline = 0
        graph.highlightp = False
        computeLimitsFromData(graph)
        graph.gDrawView()
        return graph

def regularizeData (data, color=None):
    "regular form is a list of lines, each of which is a list or list of pairs, preceded by color"
    if not isinstance(data[0], (tuple,list)):       #simple list
        return [[color, data]]
    elif isinstance(data[0][0], (tuple, list)):     # list of lists of pairs
        return [[color, d] for d in data]
    elif len(data[0]) == 2:                         # list of pairs
        return [[color, data]]
    else:                                           # list of lists
        return [[color, d] for d in data]
        
def FillInColors (data):
    for colorline in data:
        if colorline[0] == None:
            colorline[0] = FirstUnusedColor(data)
    return data

def graphData (graph):
    "Returns the data plotted in graph, with color stripped away of course"
    usegraph = chooseGraph(graph)
    dataonly = []
    for color, dlist in usegraph.data:
        dataonly.append(dlist)
    return dataonly

def FirstX (data):
    "returns the xvalue of the first point in data"
    useline = None
    for line in data:
        if line != None:
            useline = line
            break
    if useline != None:
        line = useline[1]
    if isinstance(line[0], (tuple, list)):
        firstpoint = line[0][0]
    else:
        firstpoint = 1
    return firstpoint
               
def FirstY (data):
    "returns the yvalue of the first point in data"
    useline = None
    for line in data:
        if line != None:
            useline = line
            break
    if useline != None:
        line = useline[1]
    if isinstance(line[0], (tuple, list)):
        firstpoint = line[0][1]
    else:
        firstpoint = line[0]
    return firstpoint

def graphMore (newdata, color=None, graph=None):    #<a name="graphMore"</a>[<a href="graph.html#graphMore">Doc</a>]
    addToGraph(newdata, color, graph)

def graphPointsOnly(graph=None):
    graph = chooseGraph(graph)
    graph.pointsonly = not graph.pointsonly
    graph.gDrawView()
               
def addToGraph (newdata, color=None, graph=None):    #<a name="addtograph"</a>[<a href="graph.html#addtograph">Doc</a>]
    "Adds additional data to a graph"
    if newdata == None or reduce(operator.and_, [a == None for a in newdata]):
        print("No graphing data")
    else:
        if None in newdata:
                print("Warning: Some data to be graphed was nil; ignoring")
                newdata.remove(None)
        graph = chooseGraph(graph)
        graph.data.extend(regularizeData(newdata, color))
        graph.data = FillInColors (graph.data)
        computeLimitsFromData(graph)
        graph.gDrawView()

def graphLess (colorkeyword=None, graph=None):       #<a name="graph"</a>[<a href="graph.html#graph">Doc</a>]
    "Remove a line of data points from the graph.  Defaults to last line"
    if colorkeyword == None:
        subtractFromGraph(None, graph)
    else:
        graph = chooseGraph(graph)
        removecolor = ColorFromKeyword(colorkeyword)
        linenum = 0
        for color, dlist in graph.data:
            if color == removecolor:
                subtractFromGraph(linenum, graph)
                break
            else:
                linenum +=1
        else:
            print("No such color used in this graph", colorkeyword)
    
               
def subtractFromGraph (linenum=None, graph=None):    #<a name="subtractfromgraph"</a>[<a href="graph.html#subtractfromgraph">Doc</a>]
    "Remove a line of data points from the graph. Linenum is from zero or defaults to last line"
    originalfrontwindow = Win.FrontWindow()
    graph = chooseGraph(graph)
    if linenum == None:
        linenum = len(graph.data) - 1
    num = 0
    newdata = []
    graph.data[linenum:] = graph.data[linenum+1:]
    computeLimitsFromData(graph)
    gDrawView(graph)
   
def xGraphLimits (xmin=None, xmax=None, graph=None):  #<a name="xgraphlimits"</a>[<a href="graph.html#xgraphlimits">Doc</a>]
    graph = chooseGraph(graph)
    if xmin != None or xmax != None:
        graph.autolimitsx = False
        if xmin != None:
            graph.xmin = xmin
        if xmax != None:
            graph.xmax = xmax
        gSetCoordinateSystem(graph.dataview, graph.xmin, graph.ymin, graph.xmax, graph.ymax, 'lowerLeft')
    else:
        graph.autolimitsx = True
        computeLimitsFromData(graph)
    graph.gDrawView()
    
def yGraphLimits (ymin=None, ymax=None, graph=None):  #<a name="ygraphlimits"</a>[<a href="graph.html#ygraphlimits">Doc</a>]
    graph = chooseGraph(graph)
    if ymin != None or ymax != None:
        graph.autolimitsy = False
        if ymin != None:
            graph.ymin = ymin
        if ymax != None:
            graph.ymax = ymax
        gSetCoordinateSystem(graph.dataview, graph.xmin, graph.ymin, graph.xmax, graph.ymax, 'lowerLeft')
    else:
        graph.autolimitsy = True
        computeLimitsFromData(graph)
    graph.gDrawView()

def xTickmarks (xticks=None, graph=None):             #<a name="xtickmarks"</a>[<a href="graph.html#xtickmarks">Doc</a>]
    "Sets the ticks marks and possibly resets limits."
    graph = chooseGraph(graph)
    if xticks == None:
        graph.xtickmarks = None
        if graph.data != None:
            computeLimitsFromData(graph)
    elif isinstance(xticks, (tuple, list)):
        graph.xtickmarks = regularizeTickmarks(xticks)
        graph.xmin = min(graph.xmin, MinTickmark(graph.xtickmarks))
        graph.xmax = max(graph.xmax,  MaxTickmark(graph.xtickmarks))
        gSetCoordinateSystem(graph.dataview, graph.xmin, graph.ymin, graph.xmax, graph.ymax, 'lowerLeft')
    else:               # a number
        if graph.data !=None and graph.data !=[]:
            ticks = []
            i = graph.xmin
            while i <= graph.xmax:
                ticks.append(i)
                i += xticks
            graph.xtickmarks = regularizeTickmarks(ticks)
    graph.gDrawView()

def yTickmarks (yticks=None, graph=None):            #<a name="ytickmarks"</a>[<a href="graph.html#ytickmarks">Doc</a>]
    "Sets the ticks marks and possibly resets limits."
    graph = chooseGraph(graph)
    if yticks == None:
        graph.ytickmarks = None
        if graph.data != None:
            computeLimitsFromData(graph)
    elif isinstance(yticks, (tuple, list)):
        graph.ytickmarks = regularizeTickmarks(yticks)
        if graph.data != None:
            computeLimitsFromData(graph)
        else:
            graph.ymin = min(graph.ymin, MinTickmark(graph.ytickmarks))
            graph.ymax = max(graph.ymax, MaxTickmark(graph.ytickmarks))
    else:               # a number
        if graph.data !=None and graph.data !=[]:
            ticks = []
            i = graph.ymin
            while i <= graph.ymax:
                ticks.append(i)
                i += yticks
            graph.ytickmarks = regularizeTickmarks(ticks)
    graph.gDrawView()
  

def regularizeTickmarks (ticks):
    useticks = []
    for tick in ticks:
        if isinstance(tick, (tuple, list)):
            useticks.append(tick)
        elif isinstance(tick, float):
            useticks.append([tick, str(round(tick, 3))])
        else:
            useticks.append([tick, str(tick)])          
    return useticks

def MinTickmark (ticks):
    if ticks != None and ticks !=[]:
        if isinstance(ticks[0], (tuple, list)):
            return ticks[0][0]
        else:
            return ticks[0]
        
def MaxTickmark (ticks):
    if ticks != None and ticks !=[]:
        if isinstance(ticks[-1], (tuple, list)):
            return ticks[-1][0]
        else:
            return ticks[-1]

colors = [ gColorRed(True), gColorGreen(True), gColorBlue(True), gColorBlack(True), \
               gColorYellow(True), gColorPink(True), gColorCyan(True), gColorPurple(True), \
               gColorMagenta(True), gColorOrange(True), gColorBrown(True), gColorLightBlue(True), \
               gColorGray(True), gColorDarkGreen(True), gColorTan(True) ]
                   
def nthColor (n):                    #<a name="nthColor"</a>[<a href="graph.html#nthColor">Doc</a>]
  return colors[n // length(colors)]

colorList = {'blue': gBlue, 'red': gRed, 'green': gGreen, 'black': gBlack, 'yellow': gYellow, \
        'pink': gPink, 'cyan': gCyan, 'purple': gPurple, 'magenta': gMagenta, \
        'orange': gOrange, 'brown': gBrown, 'lightBlue': gLightBlue, 'gray': gGray, \
        'darkGreen': gDarkGreen, 'tan': gTan, 'white': gWhite, \
        'lightGray': gLightGray, 'darkGray': gDarkGray }
                
def ColorFromKeyword (colorkeyword):
    color = colorList.get(colorkeyword, None)
    if color == None:
        print("Unrecognized color keyword:" ,colorkeyword)
    return color

def FirstUnusedColor (data):
    "Returns first color in the list of colors that is least used in data"
    for permittedTimesUsed in range(100):
        for color in colors:
            if TimesColorUsed(color, data) <= permittedTimesUsed:
                return color
                
def TimesColorUsed (color, data):
    count = 0
    for c, dlist in data:
        if c == color:
            count +=1
    return count

def chooseGraph (graph=None):            #<a name="choosegraph"</a>[<a href="graph.html#choosegraph">Doc</a>]
    "Select a graph based on input 'graph'"
    global GDEVICE
    glist = []
    for w in GDEVICE.childwindows:
        if isinstance(w, Graph):
            glist.append(w)
    if graph == None:               # None given - if first is a graph, use it, else make a new one
        if glist == []:
            usegraph = Graph("Graph")
        else:
            usegraph = glist[0]
    elif isinstance(graph, Graph):      # already have graph
        usegraph = graph
    elif graph == True:
        usegraph = Graph("Graph")
    elif isinstance(graph, str):        # we have a graph name
        for g in glist:
            if g.title == graph:
                usegraph = g
                break
        else:
            usegraph = Graph(graph)
    else:
        print("Error: can't choose graph", graph)
        usegraph = None
    return usegraph

def closeGraph(graph=None):
    graph.gCloseview()
        
def drawSegment (graph, x1, y1, x2, y2, color):
    l = []
    if graph.boxy:
        l.append(gDrawLine(graph.dataview, x1, y1, x2, y1, color))
        l.append(gDrawLine(graph.dataview, x2, y1, x2, y2, color))
    else:
        l.append(gDrawLine(graph.dataview, x1, y1, x2, y2, color))
    return l

def draw (graph, ylist, color):
    l = []
    for i in range(len(ylist)-1): #start from 1
        x1 = i + 1
        x2 = i + 2
        y1 = ylist[i]
        y2 = ylist[i+1]
        l.extend(drawSegment(graph, x1, y1, x2, y2, color))
    return l

def drawXY(graph, xylist, color):
    l = []
    for i in range(len(xylist)-1):
        x1, y1 = xylist[i]
        x2, y2 = xylist[i+1]
        l.extend(drawSegment(graph, x1, y1, x2, y2, color))
    return l

def calcRadius(graph):
    x0, y0, xs, ys, corner = gGetCSScale(graph.dataview)
    radius = xs / 5000.0
    if radius < .001:
        radius = .001
    if radius > .02:
        radius = .02
    return radius
    
def drawPoints(graph, ylist, color, highlight):
    radius = calcRadius(graph)
    if highlight:
        radius = 2 * radius
    l = []
    for i in range(len(ylist)):
        l.append(gDrawDisk(graph.dataview, i+1, ylist[i], radius, color))
    return l

def drawPointsXY(graph, xylist, color, highlight):
    radius = calcRadius(graph)
    if highlight:
        radius = 2 * radius
    l = []
    for i in range(len(xylist)):
        x, y = xylist[i]
        l.append(gDrawDisk(graph.dataview, x, y, radius, color))
    return l

def computeLimitsFromData (graph):
    if graph.autolimitsx:
        graph.xmin = MinTickmark(graph.xtickmarks)
        if graph.xmin == None:
            graph.xmin = FirstX(graph.data)
        graph.xmax = MaxTickmark(graph.xtickmarks)
        if graph.xmax == None:
            graph.xmax = FirstX(graph.data)
    if graph.autolimitsy:
        graph.ymin = MinTickmark(graph.ytickmarks)
        if graph.ymin == None:
            graph.ymin = FirstY(graph.data)
        graph.ymax = MaxTickmark(graph.ytickmarks)
        if graph.ymax == None:
            graph.ymax = FirstY(graph.data)
    if graph.autolimitsx or graph.autolimitsy:
        for color, dlist in graph.data:
            if not isinstance(dlist[0], (tuple, list)):
                if graph.autolimitsy:
                    for y in dlist:
                            if y < graph.ymin:
                                graph.ymin = y
                            if y > graph.ymax:
                                graph.ymax = y
                if graph.autolimitsx:
                    if 1 < graph.xmin:
                        graph.xmin = 1
                    if len(dlist) > graph.xmax:
                        graph.xmax = len(dlist)
            else:
                for x, y in dlist:
                    if graph.autolimitsy:
                        if y < graph.ymin:
                            graph.ymin = y
                        if y > graph.ymax:
                                graph.ymax = y
                    if graph.autolimitsx:
                        if x < graph.xmin:
                            graph.xmin = x
                        if x > graph.xmax:
                                graph.xmax = x
        if graph.ymin == graph.ymax:
            print("Warning: all lines are flat at", graph.ymin)
            if graph.ymax > 0:
                graph.ymin = 0
            else:
                graph.ymin = graph.ymax - 1
        gSetCoordinateSystem(graph.dataview, graph.xmin, graph.ymin, graph.xmax, graph.ymax, 'lowerLeft')
        
def gridGraph (griddensit=None, graph=None):     #<a name="gridGraph"</a>[<a href="graph.html#gridGraph">Doc</a>]
    graph = chooseGraph(graph)
    if griddensit != None:
        graph.griddensity = griddensit
    if graph.griddensity == None:
        graph.griddensity = 5
    for x, label in graph.xtickmarks:
        dx = gdCoordx(graph.dataview, x)
        if x >= graph.xmin and x <= graph.xmax:
            for dy in range(gdCoordy(graph.dataview, graph.ymax), \
                                   gdCoordy(graph.dataview, graph.ymin), \
                                   graph.griddensity):
                gdDrawPoint(graph.dataview, dx, dy, graph.maincolor)
    for y, label in graph.ytickmarks:
        dy = gdCoordy(graph.dataview, y)
        if y >= graph.ymin and y <= graph.ymax:
            for dx in range(gdCoordx(graph.dataview, graph.xmin), \
                                   gdCoordx(graph.dataview, graph.xmax), \
                                   graph.griddensity):
                gdDrawPoint(graph.dataview, dx, dy, graph.maincolor)

def drawHighlight (graph):
    if graph.highlightp and graph.highlightline != None:
        color, data = graph.data[graph.highlightline]
        graph.lasthighlight = drawLine(graph, data, gColorPen(graph, color, None, None, 2), True)
        
def removeHighlight (graph):
    if graph.lasthighlight != None:
        gDelete(graph.dataview, graph.lasthighlight)
        graph.lasthighlight = None

def drawLine (graph, line, color, highlight=False):
    if isinstance(line[0], (tuple,list)):
        if graph.pointsonly:
            return drawPointsXY(graph, line, color, highlight)
        else:
            return drawXY(graph, line, color)
    else:
        if graph.pointsonly:
            return drawPoints(graph, line, color, highlight)
        else:
            return draw(graph, line, color)

# A histogram is a graph, created in a particular way

# histogram(data, numbins, minex, maxex, graph)

def histogram (data, numbins=None, minex=None, maxex=None, color=None, hist=None):   #<a name="histogram"</a>[<a href="graph.html#histogram">Doc</a>]
    "plots histogram of data, minex <= data < maxex, in a color on a graph named hist"
    if data==None or data == []:
        print("No graphing data")
    elif len(data) == 1:
        print("Cannot histogram a single datum")
    else:
        if minex == None:
            minex = min(data)
        mx = max(data)
        if minex == mx:
            print("Error: min=max - no histogram possible")
        else:
            if isinstance(mx, int) and isinstance(minex, int):
                if maxex==None:
                    maxex = mx + 1
                if numbins == None and (mx - minex) <= 200:
                    numbins = maxex - minex
            if numbins == None:
                numbins = 30
            if maxex == None:
                maxex = mx + (.00001 * ((mx - minex) / numbins))
            hgraph = chooseGraph(hist)
            hgraph.boxy = True
            bins = [0 for i in range(numbins)]
            numtoosmall = numtoobig = 0
            scalefactor = float(numbins) / (maxex - minex)
            for d in data:
                bin = int(math.floor((d - minex) * scalefactor))
                if bin < 0:
                    numtoosmall += 1
                elif bin >= numbins:
                    numtoobig += 1
                else:
                    bins[bin] += 1
            gdata = []
            for i in range(numbins):        # prepare list of bin max, # in that bin
                x = minex + (float(i) / scalefactor)
                entry = [x , bins[i] ]
                gdata.append(entry)
            gdata.append([maxex, bins[numbins-1]])  #force the last bar to come out
            graph([gdata], color, hgraph)
            if numtoosmall != 0:
                print(numtoosmall, "data points were below the range")
            if numtoobig != 0:
                print(numtoobig, "data points were above the range")


def histogramMore  (data, numbins=None, minex=None, maxex=None, color=None, hist=None):  #<a name="histogramMore"</a>[<a href="graph.html#histogramMore">Doc</a>]
    "adds histogram of data, minex <= data < maxex, in a color to a graph named hist"
    #histogram(data, numbins, minex, maxex, color, hist)
    if data==None or data == []:
        print("No graphing data")
    elif len(data) == 1:
        print("Cannot histogram a single datum")
    else:
        if minex == None:
            minex = min(data)
        mx = max(data)
        if minex == mx:
            print("Error: min=max - no histogram possible")
        else:
            if isinstance(mx, int) and isinstance(minex, int):
                if maxex==None:
                    maxex = mx + 1
                if numbins == None and (mx - minex) <= 200:
                    numbins = maxex - minex
            if numbins == None:
                numbins = 30
            if maxex == None:
                maxex = mx + (.00001 * ((mx - minex) / numbins))
            hgraph = chooseGraph(hist)
            hgraph.boxy = True
            bins = [0 for i in range(numbins)]
            numtoosmall = numtoobig = 0
            scalefactor = float(numbins) / (maxex - minex)
            for d in data:
                bin = int(math.floor((d - minex) * scalefactor))
                if bin < 0:
                    numtoosmall += 1
                elif bin >= numbins:
                    numtoobig += 1
                else:
                    bins[bin] += 1
            gdata = []
            for i in range(numbins):        # prepare list of bin max, # in that bin
                x = minex + (float(i) / scalefactor)
                entry = [x , bins[i] ]
                gdata.append(entry)
            gdata.append([maxex, bins[numbins-1]])  #force the last bar to come out
            newdata = regularizeData([gdata],color)
            hgraph.data.extend(newdata)
            hgraph.data = FillInColors (hgraph.data)
            hgraph.gDrawView()
            if numtoosmall != 0:
                print(numtoosmall, "data points were below the range")
            if numtoobig != 0:
                print(numtoobig, "data points were above the range")
    

#Testing stuff
"""
histogram([1.2, 1.3, 2.5, 6, 20, 1.4, 5, 30, 5.5, 7, 23, 19, 15, 15], 5, None, None, 'red')
histogramMore([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30],5, None, None, 'blue')
histogramMore([1,2,11,12,13,15,21,22,23,24,25],3, None, None, 'green')

xTickmarks([0, 1, 2, 3, 4, 5],"new")
yTickmarks([0,5, 10, 15, 20, 25, 30],"new")
gridGraph(10,"new")
graph([[1,2,3,4,5],[0,1,4,9]],None, "new")
xTickmarks([(1,"st"),(2,"ar"),(3,"ts"),(4,"end")], "new")
#graph([[1, 2, 3, 4],[(1,1),(2,4),(3,6),(4,8)], [1,4,9, 25]])
g = graph([[0,1,2,3,4],[0,1,4,6,8],[0,1,4,9,27],[0,5,10,15,20],[(0,10),(1,20),(2,30)]], None, "test")
xTickmarks(1.5, "test")
yTickmarks(10, "test")

from math import *
def func1 (num):
    data = [[0. for j in range(num)] for i in range(num)]
    dx = 2. / (num - 1)
    y = - 1.
    for i in range(num):
        x = - 1
        for j in range(num):
            data[i][j] = abs(exp(-0.5 * (sqr(x) + sqr(y)))) * (1. + (cos(10 * sqrt(sqr(x) + sqr(y)))))
            x = x + dx
        y = y + dx
    return data

def sqr (x):
    return x * x
    
graph(func1(30), graph="Function")
"""
#</pre></body></html>
