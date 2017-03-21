# setup loads the major tools so that you don't need to use the module names
# you can just use the function names

# Basic stuff
from .utilities import *
from .RLinterface import RLinterface
from .traces import SimpleTraceHolder, TraceHolder
from .Tiles.tiles import CollisionTable, tiles, loadtiles, tileswrap, loadtileswrap
from .Tiles.tilesdemo import showtiles

# Gui stuff  (only for gui environments)
from .G.g import *
from .Quickgraph.graph import *
from .Quickgraph.graph3d import *

# Demo stuff
from .demo import *
