
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
from RLtoolkit.utilities import *
	
# Environment 

class MaintEnv:
    "Maintenance environment"
    def __init__(self, num=10, prob_p=.9, prob_q=.9):
        self.num_actions = 2				# number of actions (run, maint)
        self.n = num					# number of running states
        self.num_states = num + 2			# running states, end, broken
        self.p = prob_p					# prob of staying running
        self.q = prob_q					# prob of staying broken
        self.LastState = None				# last state 

def reward (env, s, a, sp):
    "reward for state transition"
    if a == 0: 						# no reward for maintenance
        r = 0
    elif sp == env.n + 1:			        # no reward for breaking
        r = 0
    else:
        r = 1						# otherwise reward 1 for running
    return r
            
def nextState (env, s, a):
    "Determines next state of environment"
    if a == 0:											# maintenance action
        news = 0										#      always causes reset
    elif s == env.n + 1:				# in broken state
        news = withProb(env.q, s, 0)			# with prob q stay there, but might fix itself
    elif s == env.n:					# final state
        news = env.n + 1				#      must break
    else:													# for anything else
        news = withProb(env.p ** (s + 1), s + 1, env.n + 1) # take chances going to next state
    return news						    #     chance of breaking increases with state
	
def do (env, verbose, a):
    "Environment does action given by agent"
    s = env.LastState
    sp = nextState(env, s, a)
    r = reward(env, s, a, sp)
    env.LastState = sp
    if verbose > 1:
        ns = env.num_states
        if sp == ns-1:
            comment = "(broken)"
        elif sp == 0:
            comment = "(start)"
        elif sp == ns-2:
            comment = "(end)"
        else:
            comment = "(running)"
        print("Environment returned sensation", sp, comment, "and reward", r)	
    return sp, r

def s0 (env, verbose):
    "Environment initial state"
    env.LastState = 0
    if verbose > 1:
        print("Starting at initial state 0")
    return 0
	
def maintenanceEnvironment(env, verbose, a=None):
    if a == None:
        s = s0(env, verbose)
        return s
    else:
        s, r = do(env, verbose, a)
        return s, r

def getMaintEnv(n=10, p=0.9, q=0.9, verbose=1):
    global env
    env = MaintEnv(n, p, q)
    env.envFunction = lambda a=None: maintenanceEnvironment(env, verbose, a)
    return env


		
