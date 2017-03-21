RLtoolkit   Version 1.0 b6  January 25, 2005

Contents:

examples - a folder of demos to run, using the toolkit
  - the maintenance example
  - mountain car (GUI and nonGUI)
   
fa - function approximation demo
   (currently only uses tile coding)
gridworld - gridworld demo
G - a general low level graphics drawing package
Quickgraph - a simple graphing package (uses g) for 2 and 3d graphs
Tiles - the tile coding package

basicclasses.py - definitions for simulation, agent and environment objects
RLinterface - contains the rl interface object and methods for it
traces - eligibility traces handling
utilities - some general utilities
guiwindow - a generic simulation window with buttons and menus
   (not yet documented for users)
demo - helps load the demos and run them
guiuser - loads all the major tools from the toolkit
  (if you do from guiuser import *, you get all the tools with no need to
   prefix module names)

These are shortcuts to some of the tool packages:
tiles - imports Tiles.tiles
g.py - imports G.g
graph.py - imports Quickgraph.graph
graph3d.py - imports Quickgraph.graph3d

There are some extra things for the RLinterface:
RLinterface2 is the interface described on the first RLAI web page as RL 6
RLinterface3 is a start of the interface described on the RL benchmarks page
rlitest2a is a simple test of RLinterface2
rlitest2b is the random walk example with RLinterface2
rlittest3a is a simple test of RLinterface3
rlitest3b is the random walk example with RLinterface3

Note: the arrangement of modules in this package is subject to change (and most likely will!) with future releases.

To use:
Move the RLtoolkit folder to your site-packages folder for Python
You can then import as you would any other package
	from RLtoolkit import Tiles.tiles as tiles
        from RLtoolkit.traces import *
        from RLtoolkit import *
        etc.
