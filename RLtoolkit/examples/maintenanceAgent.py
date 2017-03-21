
# Here we have an agent for the maintenance task.  This is a continual
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
from RLtoolkit.utilities import *

# Agent 

class TabularAgent:
    "Tabular agent for maintenance example"
    def __init__(self, num_st, num_a, alph=.01, gam=.99, ep=.1, init=0.0):
        self.num_actions = num_a			# number of actions (maint, run)
        self.num_states = num_st			# number of states	
        self.alpha = alph									# alpha (learning rate)
        self.gamma = gam									# gamma (discount rate)
        self.epsilon = ep									# epsilon (exploration rate)
        self.lastAction = None
        self.lastState = None
        init = float(init)
        self.Q = [[init for i in range(self.num_actions)] \
                  for j in range(num_st)]               # initialize Q array

class MaintenanceAgent(TabularAgent):
    "Tabular agent plus some additional stats"
    def __init__(self, num_st, num_a, alph=0.1, gam=0.99, ep=.1, \
                 interval=1000, init=0.0):
        TabularAgent.__init__(self, num_st, num_a, alph, gam, ep, init)
        self.sum_interval = interval			# set sum interval
        self.num_rewards = 0				# initialize counters
        self.sum_rewards = 0.0				#      to 0

def stateValue (agent, s):
    "State value for a state - max of action values for that state"
    return max(actionValues(agent, s))
	
def actionValues (agent, s):
    "Returns a list of action values for the agent for state s"
    return [agent.Q[s][i] for i in range(agent.num_actions)]
	
def learn (agent, verbose, s, a, r, sp):
    "Agent learn function"	
    saveq = agent.Q[s][a]  
    agent.Q[s][a] += agent.alpha * \
                (r +  (agent.gamma * stateValue(agent, sp)) \
                 - agent.Q[s][a])
    collectData(agent, s, a, r, sp)

def collectData (agent, s, a, r, sp):
    "Collect and process data"
    agent.num_rewards += 1
    agent.sum_rewards += r
    if agent.num_rewards == agent.sum_interval:
        print("Average reward over", agent.num_rewards, "steps is", \
              (agent.sum_rewards / float(agent.num_rewards)))
        agent.num_rewards = 0
        agent.sum_rewards = 0.0
	
def choose (agent, verbose, s):
    "Agent choose function"
    av = actionValues(agent, s)
    a = egreedy(agent.epsilon, agent.num_actions, av)
    if verbose > 1:
        if a == 0:
            comment = "(maint)"
        else: comment = "(run)"
        if verbose > 2:
            print("Agent chose action", a, comment, "from action values", av)
        else:
            print("Agent chose action", a, comment)
    return a
    
def maintenanceAgent(agent, verbose, s, r=None):
    if r != None:
        learn(agent, verbose, agent.lastState, agent.lastAction, r, s)
    agent.lastState = s
    if s != 'terminal':
        a = choose(agent, verbose, s)
    else:
        a = None
    agent.lastAction = a
    return a
	
def getMaintAgent(numst, numa, alph=0.01, gam=0.99, ep=0.1, init=0.0, \
                    interval=1000, verbose=1):
    global agt
    agt = MaintenanceAgent(numst, numa, alph, gam, ep, interval, init)
    agt.agentFunction = lambda s, r=None: maintenanceAgent(agt, verbose, s, r)
    return agt

def printAgentQ (agent=None):
    global agt
    if agent == None:
        agent = agt
    for i in range (agt.num_states):				
        if agt.Q[i][0] < agt.Q[i][1]:  
            comment = "prefer action 1"
        elif agt.Q[i][0] > agt.Q[i][1]: 
            comment = "prefer action 0"
        else:
            comment = "actions tied"
        print("Q values for", "%2i" % i, " ", "%2.2f" % agt.Q[i][0], "    ", "%2.2f" % agt.Q[i][1], "    ",comment)


    
		
