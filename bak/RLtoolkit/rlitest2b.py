from . import RLinterface2 as RLinterface
import random

# Random walk example using RL interface

def argmaxrandom (values):
    "Returns the index of the maximum entry in the list of values"
    best_index = 0
    best_value = values[0]
    numties = 1
    for i in range(len(values)):
	val = values[i]
	if val < best_value:			# our older value is better
	    pass
	elif val > best_value:			# the new value is better
	    best_index = i
	    best_value = val
	else:					# there is a tie; randomly pick
	    numties += 1
	    if random.randrange(0, numties) == 0:	# chose the new one
		best_index = i
		best_value = val
    return best_index				# old version returned index and value - change?


class Agent:
    "Random walk agent"

    def __init__(self, numstates, numactions=2, epsilon=0.1, alpha=0.1, gamma=0.9):
        self.numactions = numactions
        self.numstates = numstates
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.lasta = 0
        self.lasts = 0
        self.Q = [[0.0 for i in range(self.numactions)] \
                  for j in range(self.numstates)]
    
    def agentChoose(self, s):
        "Chooses the next action using epsilon-greedy"
        if random.random() < self.epsilon:
            self.lasta = random.randrange(self.numactions)
        else: 
            self.lasta = argmaxrandom(self.Q[s])
        self.lasts = s
        #print "Agent chose action", self.lasta
        return self.lasta

    def statevalue (self, s):
        if s == None:
            return 0
        elif s == 'terminal':
            return 0
        else:
            return max(self.Q[s])

    def agentLearn(self, s, a, r, sp):
        "Learns from the last action done - doing Qlearning"
        #print "Learning from state", s, "action", a, "reward", r, "next s", sp
        self.Q[s][a] += self.alpha * \
                        (r + (self.gamma * self.statevalue(sp)) \
                         - self.Q[s][a])

    def agentStart(self, s):
        "Return the first action"
        return self.agentChoose(s)

    def agentStep(self, s, r):
        "Learns and gets the next action"
        self.agentLearn(self.lasts, self.lasta, r, s)
        if s != 'terminal':
            return self.agentChoose(s)

class Environment:
    "Random walk environment"
    
    def __init__(self, numstates, numactions=2):
        self.numactions = numactions
        self.numstates = numstates
        self.curstate = self.numstates // 2 # start in the middle
        
    def envStart(self):
        "Returns the initial state"
        self.curstate = self.numstates // 2 # start in the middle
        #print "Environment initializing state to", self.curstate
        return self.curstate

    def envStep(self, a):
        "Does the action and returns the next state and reward"
        if a == 0:
            self.curstate -= 1                      # First action, go left
        elif a == self.numactions - 1:
            self.curstate += 1                      # Last action, go right
        
        if self.curstate == 0:                      # reached left end
            self.curstate = 'terminal'
            r = -1
        elif self.curstate == self.numstates - 1:   # reached right end
            self.curstate = 'terminal'
            r = 1
        else:
            r = 0
        #print "Environment did action", a, "got new state", self.curstate, "and reward", r
        return self.curstate, r

agt = Agent(10)
env = Environment(10)
rli = RLinterface.RLinterface(agt.agentStart, agt.agentStep, \
                              env.envStart, env.envStep)

for i in range(20):
    eps = rli.episode()
    print("Reward", eps[-2], "took", len(eps)//3, "steps")
    
    
