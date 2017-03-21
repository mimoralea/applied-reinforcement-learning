""" Tiles demo
This demo is good for illustrating or testing the tile routines.
The demo displays a graph where instead of lines, there is a dot for
each x,y pair in the graph. The x,y pairs are points whose tiles match the
point we are doing tiles for. There is a separate graph entry for each
of the following tile types: regular(square), stripes, diagonals, diamond,
logarithmic sized, and exponential sized.

The graph window first comes up with tiles for the point 2.0, 2.0 displayed. You
can click anywhere in the graph window to show the tiles for that point. You can
use the graph highlighting functions by pressing the space bar, and then the
arrow keys, to show the different tiles (some may be hidden by others, so this
is the only way to see some of them). There is a menu of other options for the
tile codes (e.g. collision tables, number of tilings). If you choose one of these,
a dnw window will be created, and you can move it side by side with the old one
to compare things.

When imported, a tile window is automatically created for you. There is a function to
create windows which you may wish to call:
    showtiles(numtilings, memct, floats, ints, title, start, end, intervals)
      where:
         numtilings is the number of tilings to be done
         memct is the memory size or collision table to use
         floats are the (two) floating point numbers to do tiles for
         ints is an optional list of integers to use in the tiling (defaults to none)
         start is the starting point of the tile window (defaults to 0.0)
         end is the end point of the tile window (defaults to 5.0)
         intervals is the number of intervals between whole number points (default 10)

   Note: don't make the start and end too far apart, or too many intervals
   between. The program will call the tiles function for each interval between\
   the start and end points (in each direction) for each type of tiling and
   compare it against the tiles returned by those functions for the original
   point, so if you ask for too many, it will be VERY slow.
"""

import tiles
import fancytiles
import random
import RLtoolkit.Quickgraph.graph as graph
from RLtoolkit.G.g import *


class Tileview(graph.Dataview):
    """Special graph view for tile display"""
    
    def gDrawView (self):
        self.parentgraph.gDrawView()
        pass

    def gClickEventHandler(self, x, y):
        print "clicked at ", x, y
        self.newExample(x, y)

    def newExample (self, x, y):
        global inputarray, functionapproximator, examples
        self.parentgraph.drawExample(x, y)

class TileDisplay(graph.Graph):
    
    def __init__(self, x, y, numtilings=1, memct=8192, title="Tile Display", \
                 dataviewtype=Tileview, start=0.0, end=5.0, intervals=10, **kwargs):
        title = title + " for "+str(numtilings)+" tilings"
        graph.Graph.__init__(self, title, dataviewtype, **kwargs)
        self.dataview.parentgraph = self
        self.tilex = x
        self.tiley = y
        self.numtilings = numtilings
        self.memct = memct
        self.start = start
        self.end = end
        self.intervals = intervals
        self.initDemo()

    def gDrawView(self):
        graph.Graph.gDrawView(self)
        gDrawLineR(self.dataview, self.tilex, self.tiley, 0, .2, 'black')
        gDrawLineR(self.dataview, self.tilex, self.tiley, 0, -.2, 'black')
        gDrawLineR(self.dataview, self.tilex, self.tiley, .2, 0, 'black')
        gDrawLineR(self.dataview, self.tilex, self.tiley, -.2, 0, 'black')

    def drawExample(self, x, y):
        self.tilex = x
        self.tiley = y
        graph.graph(self.calcTiledata(self.numtilings, self.memct, [x, y]), None, self)
        gDrawLineR(self.dataview, x, y, 0, .2, 'black')
        gDrawLineR(self.dataview, x, y, 0, -.2, 'black')
        gDrawLineR(self.dataview, x, y, .2, 0, 'black')
        gDrawLineR(self.dataview, x, y, -.2, 0, 'black')

    def initDemo(self):
        gClear(self)
        gClear(self.dataview)
        self.data = []
        self.drawExample(self.tilex, self.tiley)
        graph.xGraphLimits(self.start, self.end, self)
        graph.yGraphLimits(self.start, self.end, self)
        graph.graphPointsOnly(self)
        graph.xTickmarks(1, self)
        graph.yTickmarks(1, self)
        graph.gridGraph(5, self)

    def calcTiledata(self, numtilings, memct, floats, ints=[]):
        samet = []
        sametd = []
        sametbd = []
        sametdm = []
        sametl = []
        samete = []
        samets = []
        t = tiles.tiles(numtilings, memct, floats, ints)
        tsx = fancytiles.stripetiles(numtilings, memct, [floats[0]], None, ints)
        tsy = fancytiles.stripetiles(numtilings, memct, [floats[1]], None, ints)
        td = fancytiles.diagonaltiles(numtilings, memct, floats, None, ints)
        tbd = fancytiles.backdiagonaltiles(numtilings, memct, floats, None, ints)
        tdm = fancytiles.diamondtiles(numtilings, memct, floats, None, ints)
        tl = fancytiles.logtiles(numtilings, memct, floats, ints)
        te = fancytiles.exptiles(numtilings, memct, floats, ints)
        total = int((self.end - self.start) * self.intervals)
        for i in xrange(total):
            for j in xrange(total):
                x = float(i)/self.intervals + self.start
                y = float(j)/self.intervals + self.start
                newfloats = [x, y]
                if tiles.tiles(numtilings, memct, newfloats, ints) == t:
                    samet.append(newfloats)
                if fancytiles.stripetiles(numtilings, memct, [x], None, ints) == tsx or \
                   fancytiles.stripetiles(numtilings, memct, [y], None, ints) == tsy:
                    samets.append(newfloats)
                if fancytiles.diagonaltiles(numtilings, memct, newfloats, None, ints) == td:
                    sametd.append(newfloats)
                if fancytiles.backdiagonaltiles(numtilings, memct, newfloats, None, ints) == tbd:
                    sametbd.append(newfloats)
                if fancytiles.diamondtiles(numtilings, memct, newfloats, None, ints) == tdm:
                    sametdm.append(newfloats)
                if fancytiles.logtiles(numtilings, memct, newfloats, ints) == tl:
                    sametl.append(newfloats)
                if fancytiles.exptiles(numtilings, memct, newfloats, ints) == te:
                    samete.append(newfloats)
        data = [samet, samets, sametd, sametbd, sametdm, sametl, samete]
        return data
        
def showtiles(numtilings, memct, floats, ints=[], title="Tile Display", \
              start=0.0, end=5.0, intervals=10):
    w = TileDisplay(2.0, 2.0, numtilings, memct, title=title, start=start, \
                    end=end, intervals=intervals, gdViewport=(0, 20, 600, 620))
    
# should really have one for each type of tiling for test?
ctu = tiles.CollisionTable(4096, 'unsafe')
cts = tiles.CollisionTable(4096, 'safe')
ctss = tiles.CollisionTable(4096, 'super safe')

gAddMenu(GMENU, 'Tile Window', \
         [['1 tiling, memory 1024', lambda: showtiles(1, 1024, [1.0, 2.0], title="Tile Display, memory 1024")], \
          ['2 tilings, memory 1024', lambda: showtiles(2, 1024, [1.0, 2.0], title="Tile Display, memory 1024")], \
          ['4 tilings, memory 1024', lambda: showtiles(4, 1024, [1.0, 2.0], title="Tile Display, memory 1024")], \
          ['8 tilings, memory 1024', lambda: showtiles(8, 1024, [1.0, 2.0], title="Tile Display, memory 1024")], \
          ['16 tilings, memory 1024', lambda: showtiles(16, 1024, [1.0, 2.0], title="Tile Display, memory 1024")], \
          '---', \
          ['1 tiling, memory 2048', lambda: showtiles(1, 2048, [1.0, 2.0], title="Tile Display, memory 2048")], \
          ['2 tilings, memory 2048', lambda: showtiles(2, 2048, [1.0, 2.0], title="Tile Display, memory 2048")], \
          ['4 tilings, memory 2048', lambda: showtiles(4, 2048, [1.0, 2.0], title="Tile Display, memory 2048")], \
          ['8 tilings, memory 2048', lambda: showtiles(8, 2048, [1.0, 2.0], title="Tile Display, memory 2048")], \
          ['16 tilings, memory 2048', lambda: showtiles(16, 2048, [1.0, 2.0], title="Tile Display, memory 2048")], \
          '---', \
          ['1 tiling, memory 4096', lambda: showtiles(1, 4096, [1.0, 2.0], title="Tile Display, memory 4096")], \
          ['2 tilings, memory 4096', lambda: showtiles(2, 4096, [1.0, 2.0], title="Tile Display, memory 4096")], \
          ['4 tilings, memory 4096', lambda: showtiles(4, 4096, [1.0, 2.0], title="Tile Display, memory 4096")], \
          ['8 tilings, memory 4096', lambda: showtiles(8, 4096, [1.0, 2.0], title="Tile Display, memory 4096")], \
          ['16 tilings, memory 4096', lambda: showtiles(16, 4096, [1.0, 2.0], title="Tile Display, memory 4096")], \
          '---', \
          ['1 tiling, safe collision table', lambda: showtiles(1, cts, [1.0, 2.0], title="Tile Display, safe collision table")], \
          ['2 tilings, safe collision table', lambda: showtiles(2, cts, [1.0, 2.0], title="Tile Display, safe collision table")], \
          '---', \
          ['1 tiling, super safe collision table', lambda: showtiles(1, ctss, [1.0, 2.0], title="Tile Display, super safe collision table")], \
          ['2 tilings, super safe collision table', lambda: showtiles(2, ctss, [1.0, 2.0], title="Tile Display, super safe collision table")], \
          '---', \
          ['1 tiling, range -2 to 7, memory 4096', lambda: showtiles(1, 4096, [1.0, 2.0], start=-2.0, end=7.0, title="Tile Display, memory 4096")], \
          ['2 tilings, range -2 to 7, memory 4096', lambda: showtiles(2, 4096, [1.0, 2.0], start=-2.0, end=7.0, title="Tile Display, memory 4096")], \
          '---', \
          ['Quit', gQuit]])

if __name__ == "__main__":
    showtiles(1, 4096, [2.0, 2.0], title="Tile Display, memory 4096")
    graph.gStartEventLoop()
