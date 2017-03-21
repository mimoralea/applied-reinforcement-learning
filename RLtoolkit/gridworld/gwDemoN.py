""" This is gridworld code with no graphical interfaced
For a graphical interface, use gwgui.py

The walls are stateaction pairs which leave you in the same square rather than taking you
to your neighboring square.  If there were no walls, wraparound would occur at the gridworld edges
We start with walls all around the edges.

The barriers (squares you can't pass into) are overlaid on top of this.

The goal square is a terminal state.  Reward is +1 for reaching the goal, 0 else.
"""

from RLtoolkit.basicclasses import *
from .gwEnv import *
from .gwAgent import *
from .gwSim import *
from .gwio import *
import os.path

sim = None
env = None
verboseV = False

def gwInit (height=6, width=8, start=0, goal=47, alpha=0.5, gamma=0.9, \
               epsilon=0.05, agentlambda=0.8, explorationbonus=0, \
               initialvalue = .1, verbose=False):
    global env, sim, verboseV
    verboseV = verbose
    env = Gridworld(width, height, start, goal)
    agent = DynaGridAgent(4, env.numstates(), epsilon, alpha, gamma, initialvalue, \
                          agentlambda) #, expbonus)
    sim = Simulation()
    simInit(sim, agent, env, verbose)
    return sim

def gwEpisode():
    global sim
    if sim != None:
        sim.rlsim.episodeQ()
    else:
        print("You have to set up your gridworld first. Use gwInit")

def gwEpisodes(num):
    global sim
    if sim != None:
        sim.rlsim.episodesQ(num)
    else:
        print("You have to set up your gridworld first. Use gwInit")

def gwWall(square, action):
    global env
    if env != None:
        if action in range(4):
            if int(square) and square < env.numsquares and square >= 0:
                toggleWall(env, square, action)
            else:
                print("Square", square, "is not a legal square")
        else:
            print("Action", action, "is not a legal action")
    else:
        print("You have to set up your gridworld firswt. Use gwInit")

def gwBarrier(square):
    global env
    if env != None:
        if int(square) and square < env.numsquares and square >= 0:
            toggleBarrier(env, square)
        else:
            print("Square", square, "is not a legal square")
    else:
        print("You have to set up your gridworld firswt. Use gwInit")

def gwNewAgent(newlearn='onestepdyna'):
    """Legal values for newlearn are 'onestepdyna', 'qlambdareplace',
                                     'onestepq' and 'sarsalambdatraces' """
    global sim, verboseV
    changeAgentLearnMethod(sim, newlearn)
    simInit(sim, sim.agent, sim.env, verboseV)

def gwRead(file, alpha=0.5, gamma=0.9, epsilon=0.05, agentlambda=0.8, \
           explorationbonus=0, initialvalue = .1, verbose=False):
    if not os.path.isabs(file):
        file = gwFilename(file)
    list = readGridworld(file)
    genGridworldN(list, alpha, gamma, epsilon, agentlambda, explorationbonus, \
                  initialvalue, verbose)
           
def genGridworldN(alist, alpha=0.5, gamma=0.9, epsilon=0.05, \
                  agentlambda=0.8, explorationbonus=0, initialvalue = .1, \
                  verbose=False, agentclass=DynaGridAgent):
    global env, sim, verboseV
    verboseV = verbose
    width, height, startsquare, goalsquare, barrierp, wallp = getgwinfo(alist)
    env = Gridworld (width, height, startsquare, goalsquare)
    if barrierp != None:
        env.barrierp = barrierp
    if wallp != None:
        env.wallp = wallp
    agent = agentclass(4, env.numstates(), epsilon, alpha, gamma, initialvalue, \
                          agentlambda)
    sim = Simulation()
    simInit(sim, agent, env, verbose)

def gwObjRead(file, alpha=0.5, gamma=0.9, epsilon=0.05, agentlambda=0.8, \
           explorationbonus=0, initialvalue = .1, verbose=False):
    if not os.path.isabs(file):
        file = gwFilename(file)
    list = readGridworld(file)
    genObjGridworldN(list, alpha, gamma, epsilon, agentlambda, explorationbonus, \
                  initialvalue, verbose)
           
def genObjGridworldN(alist, alpha=0.5, gamma=0.9, epsilon=0.05, \
                  agentlambda=0.8, explorationbonus=0, initialvalue = .1, \
                  verbose=False):
    global env, sim, verboseV
    verboseV = verbose
    width, height, startsquare, goalsquare, barrierp, wallp = getgwinfo(alist)
    objects = alist.get('objects')
    env = ObjectGridworld (width, height, startsquare, goalsquare)
    if barrierp != None:
        env.barrierp = barrierp
    if wallp != None:
        env.wallp = wallp
    if objects != None:
        env.objects = objects
    agent = DynaGridAgent(4, env.numstates(), epsilon, alpha, gamma, initialvalue, \
                          agentlambda)
    sim = Simulation()
    simInit(sim, agent, env, verbose)

def gwDisplayPar(agent=None):
    global sim
    if agent == None:
        agent = sim.agent
    displayParameters(agent)

def gwSetPar(agent=None, alpha=None, gamma=None, epsilon=None, agentlambda=None, \
                     explorationbonus=None, initialvalue=None):
    global sim
    if agent == None:
        agent = sim.agent
    resetParameters(agent, alpha, gamma, epsilon, agentlambda, explorationbonus, \
                    initialvalue)

def gwHelp():
    print("""Gridworld demo:
   To set up your gridworld, use
      gwInit(height, width, start, goal, alpha, gamma, epsilon,
             agentlambda, explorationbonus, initialvalue, verbose)
         numepisodes is the number of episodes to run (default is 1)
         height is the number of squares high the gridworld is (default is 6)
         width is the number of squares wide the gridworld is (default is 8)
           squares are numbered from 0 to height x width - 1
         start is the square the agent starts from (default 0)
         goal is the goal square (default 47)
         alpha is the learning rate (default 0.5)
         gamma is the discount rate (default 0.9)
         epsilon is the exploration rate (default 0.05)
         agentlambda is lambda (default 0.8)
         explorationbonus is the exploration bonus (default 0)
         initial value is the value to start the Q values at (default is 0.1)
         verbose is whether or not to print each action and state (default False)
    Note: squares are numbered from 0 to height x width - 1

   Optionally add walls and barriers to your gridworld:
      The walls are stateaction pairs which leave you in the same square rather
      than taking you to your neighboring square.  If there were no walls,
      wraparound would occur at the gridworld edges. We start with walls all around
      the edges. The barriers (squares you can't pass into) are overlaid on top of this.
      
      gwWall(square, action)
         adds a wall in the square specified by square for the action specified
         by action (0-left, 1-up, 2-right, 3-down)
         If there is already a wall there, this removes it.
      gwBarrier(square)
         makes square a barrier square (filled in). If the square was already a barrier,
         this makes it a normal square (non barrier)

   Albernatively, read in a gridworld using:
      gwRead("filename", alpha, gamma, epsilon, agentlambda, explorationbonus, 
              initialvalue, verbose)
         where filename specifies one of the files in the Gridworlds folder
           (e.g. "gw16x10") or the entire pathname of a file anywhere else
         the other parameters are as for gwInit, above

   The default agent uses one step dyna as its learning method. To change the agent:
      gwNewAgent(newlearn)
         where newlearn is one of
            'onestepq' - one step Q learning
            'qlambdareplace' - q lambda replacing traces
            'onestepdyna' - one step dyna
            'sarsalambdatraces' - sarsa lambda with traces
      gwSetPar(agent, alpha, gamma, epsilon, agentlambdam explorationbonus, initialvalue)
         changes specified parameters. The agent defaults to the current agent.
      gwDisplayPar(agent)
         displays the type and parameters for the agent specified
           (defaults to the current agent)

   To run simulations on the gridworld (after gwInit or gwRead has been run), use:
      gwEpisode()      runs one episode
      gwEpisodes(num)  runs num episodes
   both return the number of steps required to reach the goal for each episode
   """)

gwHelp()
