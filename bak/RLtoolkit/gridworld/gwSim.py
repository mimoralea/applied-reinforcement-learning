""" Simulation code for running gridworld
"""

from RLtoolkit.RLinterface import RLinterface
from .gwAgent import *
from .gwEnv import *

SIM = None
 
def simInit (sim, agent, env, verbose=False):
    global SIM
    SIM = sim
    sim.episodenum = 0
    sim.episodestepnum = 0
    sim.stepnum = 0
    sim.rlsim = RLinterface(lambda s, r=None: agent.agentfn(verbose, s, r), \
                            lambda a=None: env.envfn(verbose, a))
    sim.agent = agent
    sim.env = env
    env.sim = sim
    agent.sim = sim
    agent.agentInit()

def resetSim (sim):
    agent = sim.agent
    sim.episodenum = 0
    sim.episodestepnum = 0
    sim.stepnum = 0
    agent.agentInit()
    agent.Q = [[agent.initialvalue for a in range(agent.numactions)] \
               for s in range(agent.numstates)]
