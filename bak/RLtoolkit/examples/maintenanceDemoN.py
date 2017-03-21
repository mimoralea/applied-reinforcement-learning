
# Here we have an example MDP: the maintenance task.  This is a continual
# task, with no episodes or resets.  You are running a machine to maximize reward.
# The only way to get rewards is to operate your machine.  If that works well,
# you earn $1 and proceed from your current state i to i+1.  But the machine 
# also might break.  Then you go to a broken state (with zero reward), where you
# stay with probability Q until you get out to state 0.  If you chose not to 
# operate the machine, you can instead do maintenance.  This doesn't get any 
# reward, and takes you back to state 0.  The probability that operating the 
# machine will work is P**(i+1), except for state N, which never works.  
# Counting the broken state, there are N+2 states

# This version does not use the numarray package
		
from random import randrange, random
from RLtoolkit.RLinterface import RLinterface
from .maintenanceAgent import *
from .maintenanceEnv import *

def maintInit (n=10, p=.9, q=.9, alpha=.01, gamma=.99, epsilon=.1, init=0.0, \
               interval =1000, verbose=1):
    global rli, agt
    env = getMaintEnv(n, p, q, verbose)
    agt = getMaintAgent(env.num_states, env.num_actions, alpha, gamma, epsilon , \
                                    init, interval, verbose)
    rli = RLinterface(agt.agentFunction, env.envFunction)

def maintSteps(steps=10001):
    "Runs num steps of the maintenance example"
    global rli
    if rli == None:
        print("You must run initialize with maintInit first")
    else:
        rli.steps(steps)
    
def maintTest (n=10, p=.9, q=.9, alpha=.01, gamma=.99, epsilon=.1, init=0.0, \
               interval=1000, verbose=1, steps=10001):
    "Main routine to run the maintenance example"
    global agt
    maintInit(n, p, q, alpha, gamma, epsilon, init, interval, verbose)
    maintSteps(steps)
    if verbose > 0:
        print("n", n, "p", p, "q", q, "alpha", alpha, "gamma", gamma, "epsilon", epsilon)
        printAgentQ(agt)
        
def maintHelp():
    print("""Maintenance example demo:
    Use functions:
        maintInit(n, p, q, alpha, gamma, epsilon, verbose, interval)
          Initializes the agent and sets things up
        maintSteps(steps)
          Runs steps steps of the maintenance example
        maintTest(n, p, q, alpha, gamma, epsilon, verbose, steps, interval)
          Initializes and then runs steps steps of the maintenance example

          n = number of running states (total states =n+2) (default=10)
          p = probability of staying running (default 0.9) (exponential)
          q = probability of staying broken (default 0.9)
          alpha = learning rate (default .01)
          gamma = discount rate (default .99)
          epsilon = exploration rate (default 0.1)
          verbose = how much to print
              0(quiet), 1(averages-default), 2(details), 3(more details)
          steps = number of steps to simulate (defaults to 10001)
          interval = averaging interval to do statistics over (defaults to 1000)
    """)
          
maintHelp()
		
