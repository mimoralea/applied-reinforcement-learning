"""
This is gridworld code with a graphical display and user interface.
For non graphical gridworld, use gwDemoN.py

There are three main objects:
   Gridworld          Just the environment with no graphics stuff
   Gridworldview      A gridworld with view (graphics related stuff)
   GridworldWindow    A simulation window to hold the gridworldview with buttons for simulation

The walls are stateaction pairs which leave you in the same square rather
than taking you to your neighboring square.  If there were no walls, wraparound
would occur at the gridworld edges.
We start with walls all around the edges.

The barriers (squares you can't pass into) are overlaid on top of this.

The goal square is a terminal state.  Reward is +1 for reaching the goal, 0 else.
"""


###

from .gwguimain import *
from .gwobject import *

def runDemo():
   makeGridworldSimulation(16, 16, 87, 15, 30)
   gMainloop()

def runObjDemo():
    makeObjectGridworldSimulation(16, 16, 87, 15, 30)
    gMainloop()

if __name__ == '__main__':
    runObjDemo()
