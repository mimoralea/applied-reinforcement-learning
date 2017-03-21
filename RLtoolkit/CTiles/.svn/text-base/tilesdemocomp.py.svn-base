""" Tiles demo with both c and python tiles
Exactly the same as the regular tile demo, but points are only added to the
various graph parts if both the c and python versions of tiles agree. Anything
else goes into the "c only" or "python only" lists, and those are added as
separate graphical objects.
"""

import RLtoolkit.Tiles.tiles as tiles
import RLtoolkit.Tiles.fancytiles as fancytiles
import RLtoolkit.CTiles.tiles as ctiles
import RLtoolkit.CTiles.fancytiles as fancytilesc
import random
import RLtoolkit.Quickgraph.graph as graph
from RLtoolkit.G.g import *

class Tileview(graph.Dataview):
    """Special graph view for Tile Display comparison"""
    
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
    
    def __init__(self, x, y, numtilings=1, memct=8192, title="Tile Display comparison", \
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
        #graph.xGraphLimits(0.0, 5.0, self)
        #graph.yGraphLimits(0.0, 5.0, self)
        graph.xGraphLimits(self.start, self.end, self)
        graph.yGraphLimits(self.start, self.end, self)
        graph.graphPointsOnly(self)
        graph.xTickmarks(1, self)
        graph.yTickmarks(1, self)
        graph.gridGraph(5, self)

    def calcTiledata(self, numtilings, memct, floats, ints=[]):
        global ctss, ctssc, cts, ctsc, ctu, ctuc
        if memct == ctss:
            memctc = ctssc
        elif memct == ctu:
            memctc = ctuc
        elif memct == cts:
            memctc = ctsc
        else:
            memctc = memct
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
        ct = ctiles.tiles(numtilings, memctc, floats, ints)
        ctsx = fancytilesc.stripetiles(numtilings, memctc, [floats[0]], None, ints)
        ctsy = fancytilesc.stripetiles(numtilings, memctc, [floats[1]], None, ints)
        ctd = fancytilesc.diagonaltiles(numtilings, memctc, floats, None, ints)
        ctbd = fancytilesc.backdiagonaltiles(numtilings, memctc, floats, None, ints)
        ctdm = fancytilesc.diamondtiles(numtilings, memctc, floats, None, ints)
        ctl = fancytilesc.logtiles(numtilings, memctc, floats, ints)
        cte = fancytilesc.exptiles(numtilings, memctc, floats, ints)
        csame = []
        psame = []
        total = int((self.end - self.start) * self.intervals)
        for i in xrange(total):
            for j in xrange(total):
                x = float(i)/self.intervals + self.start
                y = float(j)/self.intervals + self.start
                newfloats = [x, y]
                tnew = tiles.tiles(numtilings, memct, newfloats, ints)
                ctnew = ctiles.tiles(numtilings, memctc, newfloats, ints)
                if tnew == t and ctnew == ct:
                    samet.append(newfloats)
                elif tnew == t:
                    psame.append(newfloats)
                    #print "regular tiles same in python but not c", x, y, t, tnew, ct, ctnew
                elif ctnew == ct:
                    csame.append(newfloats)
                    #print "regular tiles same in c but not python", x, y, t, tnew, ct, ctnew
                if fancytiles.stripetiles(numtilings, memct, [x], None, ints) == tsx or \
                   fancytiles.stripetiles(numtilings, memct, [y], None, ints) == tsy:
                    samets.append(newfloats)
              
                tdnew = fancytiles.diagonaltiles(numtilings, memct, newfloats, None, ints)
                ctdnew = fancytilesc.diagonaltiles(numtilings, memctc, newfloats, None, ints)
                if tdnew == td and ctdnew == ctd:
                    sametd.append(newfloats)
                elif tdnew == td:
                    psame.append(newfloats)
                    #print "diagonal tiles same in python but not c", x, y, td, tdnew, ctd, ctdnew
                elif ctdnew == ctd:
                    csame.append(newfloats)
                    #print "diagonal tiles same in c but not python", x, y, td, tdnew, ctd, ctdnew
                tbdnew = fancytiles.backdiagonaltiles(numtilings, memct, newfloats, None, ints)
                ctbdnew = fancytilesc.backdiagonaltiles(numtilings, memctc, newfloats, None, ints)
                if tbdnew == tbd and ctbdnew == ctbd:
                    sametbd.append(newfloats)
                elif tbdnew == tbd:
                    psame.append(newfloats)
                    print "back diagonal tiles same in python but not c", x, y, tbd, tbdnew, ctbd, ctbdnew
                elif ctbdnew == ctbd:
                    csame.append(newfloats)
                    print "back diagonal tiles same in c but not python", x, y, tbd, tbdnew, ctbd, ctbdnew

                tdmnew = fancytiles.diamondtiles(numtilings, memct, newfloats, None, ints)
                ctdmnew = fancytilesc.diamondtiles(numtilings, memctc, newfloats, None, ints)
                if tdmnew == tdm and ctdmnew == ctdm:
                    sametdm.append(newfloats)
                elif tdmnew == tdm:
                    psame.append(newfloats)
                    #print "diamond tiles same in python but not c", x, y, tdm, tdmnew, ctdm, ctdmnew
                elif ctdmnew == ctdm:
                    csame.append(newfloats)
                    #print "diamond tiles same in c but not python", x, y, tdm, tdmnew, ctdm, ctdmnew
                tlnew = fancytiles.logtiles(numtilings, memct, newfloats, ints)
                ctlnew = fancytilesc.logtiles(numtilings, memctc, newfloats, ints)
                if tlnew == tl and ctlnew == ctl:
                    sametl.append(newfloats)
                elif tlnew == tl:
                    psame.append(newfloats)
                    #print "log tiles same in python but not c", x, y, tl, tlnew, ctl, ctlnew
                elif ctlnew == ctl:
                    csame.append(newfloats)
                    #print "log tiles same in c but not python", x, y, tl, tlnew, ctl, ctlnew
                tenew = fancytiles.exptiles(numtilings, memct, newfloats, ints)
                ctenew = fancytilesc.exptiles(numtilings, memctc, newfloats, ints)
                if tenew == te and ctenew == cte:
                    samete.append(newfloats)
                elif tenew == te:
                    psame.append(newfloats)
                    #print "exp tiles same in python but not c", x, y, te, tenew, cte, ctenew
                elif ctenew == cte:
                    csame.append(newfloats)
                    #print "exp tiles same in c but not python", x, y, te, tenew, cte, ctenew

        data = [samet, samets, sametd, sametbd, sametdm, sametl, samete, psame, csame]
        return data
        
def showtiles(numtilings, memct, floats, ints=[], title="Tile Display comparison", \
              start=0.0, end=5.0, intervals=10):
    w = TileDisplay(2.0, 2.0, numtilings, memct, title=title, start=start, \
                    end=end, intervals=intervals, gdViewport=(0, 20, 600, 620))
    
# should really have one for each type of tiling for test?
ctu = tiles.CollisionTable(4096, 'unsafe')
cts = tiles.CollisionTable(4096, 'safe')
ctss = tiles.CollisionTable(4096, 'super safe')
ctuc = ctiles.CollisionTable(4096, 'unsafe')
ctsc = ctiles.CollisionTable(4096, 'safe')
ctssc = ctiles.CollisionTable(4096, 'super safe')

gAddMenu(GMENU, 'Tile Window', \
         [['1 tiling, memory 1024', lambda: showtiles(1, 1024, [1.0, 2.0], title="Tile Display comparison, memory 1024")], \
          ['2 tilings, memory 1024', lambda: showtiles(2, 1024, [1.0, 2.0], title="Tile Display comparison, memory 1024")], \
          ['4 tilings, memory 1024', lambda: showtiles(4, 1024, [1.0, 2.0], title="Tile Display comparison, memory 1024")], \
          ['8 tilings, memory 1024', lambda: showtiles(8, 1024, [1.0, 2.0], title="Tile Display comparison, memory 1024")], \
          ['16 tilings, memory 1024', lambda: showtiles(16, 1024, [1.0, 2.0], title="Tile Display comparison, memory 1024")], \
          '---', \
          ['1 tiling, memory 2048', lambda: showtiles(1, 2048, [1.0, 2.0], title="Tile Display comparison, memory 2048")], \
          ['2 tilings, memory 2048', lambda: showtiles(2, 2048, [1.0, 2.0], title="Tile Display comparison, memory 2048")], \
          ['4 tilings, memory 2048', lambda: showtiles(4, 2048, [1.0, 2.0], title="Tile Display comparison, memory 2048")], \
          ['8 tilings, memory 2048', lambda: showtiles(8, 2048, [1.0, 2.0], title="Tile Display comparison, memory 2048")], \
          ['16 tilings, memory 2048', lambda: showtiles(16, 2048, [1.0, 2.0], title="Tile Display comparison, memory 2048")], \
          '---', \
          ['1 tiling, memory 4096', lambda: showtiles(1, 4096, [1.0, 2.0], title="Tile Display comparison, memory 4096")], \
          ['2 tilings, memory 4096', lambda: showtiles(2, 4096, [1.0, 2.0], title="Tile Display comparison, memory 4096")], \
          ['4 tilings, memory 4096', lambda: showtiles(4, 4096, [1.0, 2.0], title="Tile Display comparison, memory 4096")], \
          ['8 tilings, memory 4096', lambda: showtiles(8, 4096, [1.0, 2.0], title="Tile Display comparison, memory 4096")], \
          ['16 tilings, memory 4096', lambda: showtiles(16, 4096, [1.0, 2.0], title="Tile Display comparison, memory 4096")], \
          '---', \
          ['1 tiling, safe collision table', lambda: showtiles(1, cts, [1.0, 2.0], title="Tile Display comparison, safe collision table")], \
          ['2 tilings, safe collision table', lambda: showtiles(2, cts, [1.0, 2.0], title="Tile Display comparison, safe collision table")], \
          '---', \
          ['1 tiling, super safe collision table', lambda: showtiles(1, ctss, [1.0, 2.0], start=-2.0, end=7.0, title="Tile Display comparison, super safe collision table")], \
          ['2 tilings, super safe collision table', lambda: showtiles(2, ctss, [1.0, 2.0], title="Tile Display comparison, super safe collision table")], \
          '---', \
          ['Quit', gQuit]])

showtiles(1, 4096, [2.0, 2.0], title="Tile Display comparison, memory 4096", start=-2.0, end=7.0)
graph.gStartEventLoop()
