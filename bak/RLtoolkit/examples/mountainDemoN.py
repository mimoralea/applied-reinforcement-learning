# This is an example program for reinforcement learning with linear function
# approximation. The code follows the psuedo-code for linear, gradient-descent
# Sarsa(*lambda*) given in Figure 8.8 of the book "Reinforcement Learning: An
# Introduction", by Sutton and Barto. One difference is that we use the
# implementation trick mentioned on page 189 to only keep track of the traces
# that are larger than "min-trace".

# This code can be used for either non-graphical or graphical simulations.
# For graphical, import mountainGui, which also imports this file.
# For nongraphical, use mountainNongui, or simply load this file and call the
# function mCarTest(numEpisodes, maxSteps, epsilon, alpha)
#  (only numEpisodes is required)

# After loading, you need to call Setup, after which you will
# be able to call mcEpisode to generate episodes of Mountain Car. mcEpisode
# returns the length of the episode and prints it out. 

# The code below is in three main parts: 1) General RL code, 2) Mountain Car
# code, and 3) code for the graphical display of the mountain car. Earlier parts
# of the code can be understood independently of later parts. 

# Written by Rich Sutton 12/17/00
# Converted to Python in April, 2004
# Modified to use the RL interface in April 2004

from RLtoolkit.RLinterface import RLinterface
from .mountainEnv import *
from .mountainAgent import *

def mcEpisode (maxsteps=10000):	
    "Runs one episode of mountain car"
    global rli
    if rli == None:
        rli = RLinterface(mountainAgent, mountainEnv)
    rli.episode(maxsteps)
    st, ep, epst = curStats()
    print("Used", epst, "steps")
    return epst
	
def mcEpisodes (numEpisodes, maxsteps=2000):
    "Simulates num episodes of mountain car"
    global rli
    if rli == None:
        rli = RLinterface(mountainAgent, mountainEnv)
    eps = []
    for i in range(numEpisodes):
	eps.append(mcEpisode(maxsteps))
    return eps

def mcInit (epsil=0.01, alph=0.5):
    "Initializes the agent and gets ready to run"
    global rli
    setAlpha(alph)
    setEpsilon(epsil)
    setupAgent()
    rli = RLinterface(mountainAgent, mountainEnv)
    return rli

def mcTest (numEpisodes, maxsteps=2000, epsil=0.01, alph=0.5):
	"""Runs numEpisodes episodes, each with maxSteps, and returns a list of 
	    the number of steps taken by each episode"""
	mcInit(epsil, alph)
	return(mcEpisodes(numEpisodes, maxsteps))

def mcHelp():
    print("""Mountain Car Demo:
   To run:
      mcInit(epsilon, alpha)
        Initializes the agent and gets things started
          epsilon = exploration rate (defaults to 0.01)
          alpha = learning rate (defaults to 0.9)
      mcEpisode(maxsteps)
        Simulates one episode of mountain car
          maxsteps is the maximum steps for the episode (defaults to 2000)
      mcEpisodes(num, maxsteps)
        Simulates num episodes of mountain car
          num is the number of episodes to run
          maxsteps is the maximum steps for each episode (defaults to 2000)
      mcTest(numepisodes, maxsteps, epsilon, alpha)
        Initializes the agent and runs numepisodes of mountain car.
        Returns a list of the number of steps required per episode.
           numepisodes is the number of episodes to run
           maxsteps is the maximum number of steps per episode (default 2000)
           epsilon is the exploration rate (default is 0.01)
           alpha is the learning rate (default is 0.9)
    """)

mcHelp()

import time

def mcTime(episodes=200):
    #seed(64497)
    s=time.clock()
    mcEpisodes(episodes)
    e=time.clock()
    print("Used", e-s, "seconds for", episodes, "episodes")
    return e-s


