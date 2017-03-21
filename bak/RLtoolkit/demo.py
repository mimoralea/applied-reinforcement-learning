# Demo loading

# demos()                    gives a list of available demos
# demos('demoname')          displays some information about that demo
# demos('demoname', 'run')   loads and runs the demo
#   GUI demos will start immediately
#   nonGUI demos print help information on how to run the demo

from . import examples
from . import gridworld
from . import fa
import sys, os

def mountainCarGuiDemo():
    from .examples.mountainDemoG import runDemo
    runDemo()

def mountainCarNonGuiDemo():
    global mcTest, mcEpisodes, mcEpisode, mcInit, mcHelp
    from .examples.mountainDemoN import mcTest, mcEpisodes, mcEpisode, mcInit, mcHelp
    mcTest = examples.mountainDemoN.mcTest
    mcEpisodes = examples.mountainDemoN.mcEpisodes
    mcEpisode = examples.mountainDemoN.mcEpisode
    mcInit = examples.mountainDemoN.mcInit
    mcHelp = examples.mountainDemoN.mcHelp

def gridworldGuiDemo():
    from .gridworld.gwDemoG import runDemo
    runDemo()

def gridworldObjGuiDemo():
    from .gridworld.gwDemoG import runObjDemo
    runObjDemo()

def gridworldNonGuiDemo():
    global gwEpisode, gwEpisodes, gwInit, gwWall, gwBarrier, gwRead, gwNewAgent, \
           gwDisplayPar, gwSetPar, gwObjRead
    from .gridworld.gwDemoN import gwEpisode, gwEpisodes, gwInit, gwWall, \
         gwBarrier, gwHelp, gwRead, gwNewAgent, gwDisplayPar, gwSetPar, gwObjRead
    gwEpisode = gridworld.gwDemoN.gwEpisode
    gwEpisodes = gridworld.gwDemoN.gwEpisodes
    gwInit = gridworld.gwDemoN.gwInit
    gwHelp = gridworld.gwDemoN.gwHelp
    gwWall = gridworld.gwDemoN.gwWall
    gwBarrier = gridworld.gwDemoN.gwBarrier
    gwRead = gridworld.gwDemoN.gwRead
    gwNewAgent = gridworld.gwDemoN.gwNewAgent
    gwDisplayPar = gridworld.gwDemoN.gwDisplayPar
    gwSetPar = gridworld.gwDemoN.gwSetPar
    gwObjRead = gridworld.gwDemoN.gwObjRead

def functionApproximationDemo():
    from .fa.demo import faDemo
    faDemo()

def maintenanceEgDemo():
    global maintInit, maintSteps, maintTest, maintHelp
    from .examples.maintenanceDemoN import maintInit, maintSteps, maintTest, maintHelp
    maintInit = examples.maintenanceDemoN.maintInit
    maintHelp = examples.maintenanceDemoN.maintHelp
    maintTest = examples.maintenanceDemoN.maintTest
    maintSteps = examples.maintenanceDemoN.maintSteps

demoFn = {'mcg': mountainCarGuiDemo, \
          'mcn': mountainCarNonGuiDemo, \
          'gwg': gridworldGuiDemo, \
          'gwog': gridworldObjGuiDemo, \
          'gwn': gridworldNonGuiDemo, \
          'fa' : functionApproximationDemo, \
          'maint': maintenanceEgDemo, \
          'maint': maintenanceEgDemo}

demoDoc = {'mcg': "Mountain Car with GUI interface", \
           'mcn': "Mountain Car with non GUI interface", \
           'maint': "Maintenance Example", \
           'fa': "Function Approximation", \
           'gwg': "Gridworld with GUI interface", \
           'gwn': "Gridworld with non GUI interface", \
           'gwog': "Gridworld with rewards (objects) with GUI interface"}

demoHelp = {"maint" : """Maintenance example:
  This is a continual task, with no episodes or
  resets.  You are running a machine to maximize reward.
  The only way to get rewards is to operate your machine.  If that works well,
  you earn $1 and proceed from your current state i to i+1.  But the machine
  also might break.  Then you go to a broken state (with zero reward), where you
  stay with probability Q until you get out to state 0.  If you chose not to
  operate the machine, you can instead do maintenance.  This doesn't get any
  reward, and takes you back to state 0.  The probability that operating the
  machine will work is P**(i+1), except for state N, which never works.
  Counting the broken state, there are N+2 states- an MDP with a machine which
  breaks with probability p, stays broken with probability q. Actions
  are run and do maintenance. Rewards are for running only.""", \
            "mcn" : """Mountain Car Demo, non GUI interface:
  This is an example program for reinforcement learning with linear function
  approximation (tiles) and sarsa lambda with traces. A car is at the bottom
  of a deep valley and must try to get out. It has 3 actions: reverse thrust,
  forward thrust, and coast.
            """, \
            "mcg" : """Mountain Car Demo, GUI interface:
  This is an example program for reinforcement learning with linear function
  approximation (tiles) and sarsa lambda with traces. A car is at the bottom
  of a deep valley and must try to get out. It has 3 actions: reverse thrust,
  forward thrust, and coast. The GUI interface shows the car from the side view,
  top view, and also shows the 3D surface of the value function. You can run
  a single step, single episode or just keep running episode after episode
  with the interface.
            """, \
            "gwn" : """Gridworld example, non GUI interface:
  This is an episodic task with a dyna agent acting in a gridworld environment.
  The agent's goal is to go from the start square to the goal square. Actions 
  are right, left, up and down. You can specify the dimensions of the world, as
  well as walls and barriers within the world. Rewards are +1 for reaching the
  goal, 0 otherwise.""", \
            "gwg" : """Gridworld example, GUI interface:
  This is an episodic task with a dyna agent acting in a gridworld environment.
  The agent's goal is to go from the start square to the goal square. Actions 
  are right, left, up and down. You can specify the dimensions of the world, as
  well as walls and barriers within the world. Rewards are +1 for reaching the
  goal, 0 otherwise. The GUI interface visually shows the agent learning and
  also allows you to set many details of the agent, step through simulations,
  start new simulations, visually set up your gridworld, save a gridworld, and
  more""", \
            "gwog" : """Gridworld with rewards (objects) example, GUI interface:
  This is an episodic task with a dyna agent acting in a gridworld environment.
  The agent's goal is to go from the start square to the goal square. Actions 
  are right, left, up and down. You can specify the dimensions of the world, as
  well as walls and barriers within the world. Permanent and consumable objects
  can be added to the gridworld which give positive or negative rewards
  when the agent lands on them. Reward is +1 for reaching the goal.
  The GUI interface visually shows the agent learning and
  also allows you to set many details of the agent, step through simulations,
  start new simulations, visually set up your gridworld, save a gridworld, and
  more""", \
            "fa" : """Function Approximation Demo:
  This GUI demo shows function approximation in action on a graph. Currently it
  uses tiling as the representation, but other methods will be available soon.
  You can modify various aspects of the representation method and function
  approximator to see what effects they have."""}

def demos(d=None, do=None):
    "Print demo info o run specific demo"
    global demoDoc, demoFn, demoHelp
    if d == None or d == 'help':
        for k, v in list(demoDoc.items()):
            print(k, " \t", v)
        print(" ")
        print("""For more information on any demo, use demos("demoname")""")
        print("""To run a demo, use demos("demoname", "run")""")
    elif do == "run":
        fn = demoFn.get(d)
        if fn == None:
            print("There is no demo called", d)
        else:
            fn()
    else:
        info = demoHelp.get(d)
        if info == None:
            print("Sorry, no more information for ", d)
        else:
            print(info)

print("To get a list of demos available, use demos()")

