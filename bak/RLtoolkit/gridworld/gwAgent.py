""" This is gridworld code for use standalone, with or without display onto 
an arbitrary gview, or in conjunction with the standard RL interface.  For standalone use with a display, a simple gridworldwindow is provided.

There are three main objects:
   Gridworld          Just the environment with no graphics stuff
   Gridworldview     A gridworld with view (graphics related stuff)
   Gridworldwindow   A gridworldview that happens to be a window

The walls are stateaction pairs which leave you in the same square rather than taking you to your neighboring square.  If there were no walls, wraparound would occur at the gridworld edges# we start with walls all around the edges.

The barriers (squares you can't pass into) are overlaid on top of this.

The goal square is a terminal state.  Reward is +1 for reaching the goal, 0 else.
"""

from RLtoolkit.utilities import *
from RLtoolkit.basicclasses import *
from random import *
from math import *
import operator

lasts = 0
lasta = 0

changeDiff = 0.01      # difference in Q values needed to notice change

###

class GridAgent (Agent):
    def __init__(self, numactions, numstates, epsilon=0.05, alpha=0.5, \
                 gamma=.9, initialvalue=0.1, agentlambda=0.8):
        Agent.__init__(self)
        self.alpha = alpha
        self.initialvalue = initialvalue
        self.gamma = gamma
        self.epsilon = epsilon
        self.agentlambda = agentlambda
        self.recentsensations = []
        self.recentactions = []
        self.numactions = numactions
        self.numstates = numstates
        self.Q = [[self.initialvalue for i in range(self.numactions)] \
                  for j in range(self.numstates)]
        self.savedq = [[self.initialvalue for i in range(self.numactions)] \
                  for j in range(self.numstates)]
        self.changedstates = []
 
    def agentStartEpisode (self, sensation):
        self.recentsensations = []
        self.recentactions = []

    def agentchangestate(self, s):
        if not s in  self.changedstates:
            self.changedstates.append(s)
    
    def actionvalues (self, s):
        return [self.Q[s][a] for a in range(self.numactions)]

    def statevalue (self, s):
        if s == None:
            return 0
        elif s == 'terminal':
            return 0
        else:
            return max(self.actionvalues(s))

    def policy (self, state):
        return egreedy(self.epsilon, self.numactions, self.actionvalues(state))
    
    def agentChoose (self, sprime):    # epsilon greedy
        self.recentsensations = [sprime] + self.recentsensations
        if sprime != 'terminal':
            self.recentactions = [self.policy(sprime)] + self.recentactions
            return self.recentactions[0]

    def agentLearn (self, s, a, reward, sprime): #default is one step q
        self.Q[s][a] += self.alpha * (r + \
                                        (self.gamma * self.statevalue(sprime)) \
                                        - self.Q[s][a])

    def agentInit(self):
        self.recentsensations = []
        self.recentactions = []
        pass

    def agentfn(self, verbose, s, r=None):
        global lasts, lasta
        simcollect(self.sim, lasts, lasta, r, s)
        if r != None:
            self.agentLearn(lasts, lasta, r, s)
        else:
            self.agentStartEpisode(s)
        if s != 'terminal':
            a = self.agentChoose(s) 
            lasts, lasta = s, a
            if verbose:
                print("Agent chose action", a)
            return a
        else:
            return None
        
class SarsaGridAgent(GridAgent):
    def agentLearn (self, s1, a1, r, sprime):    # Sarsa
        global changeDiff
        if sprime != 'terminal':
            aprime = self.agentChoose(sprime)
            aprimeq = self.Q[sprime][aprime]
        else:
            aprimeq = 0
        alphadelta = self.alpha * (r + (self.gamma * aprimeq) - self.Q[s1][a1])
        oldq = self.Q[s1][a1]
        self.Q[s1][a1] += alphadelta 
        if abs(self.Q[s1][a1] - oldq) > changeDiff:
            self.agentchangestate(s1)

    def agentfn(self, verbose, s, r=None):
        global lasts, lasta
        simcollect(self.sim, lasts, lasta, r, s)
        if debugmode():
            print("agentfn", s, r)
        if r != None:
            self.agentLearn(lasts, lasta, r, s) # does action choice as well
        else:
            self.agentStartEpisode(s)
            a = self.agentChoose(s)             # first action
            if debugmode():
                print("st", self.recentsensations, "ac", self.recentactions)
        if s != 'terminal':
            a = self.recentactions[0]
            lasts, lasta = s, a
            if verbose:
                print("Agent chose action", a)
            return a
        else:
            return None

class SarsaLambdaGridAgent(SarsaGridAgent):
    def agentLearn (self, s1, a1, r, sprime):  # Sarsa(lambda), replace traces
        global changeDiff
        senses = self.recentsensations
        actions = self.recentactions
        if sprime != 'terminal':
            aprime = self.agentChoose(sprime)
            aprimeq = self.Q[sprime][aprime]
        else:
            aprimeq = 0
        alphadelta = self.alpha * (r + (self.gamma * aprimeq) - self.Q[s1][a1])
        if debugmode():
            print("states", senses)
            print("actions", actions)
            print("s1",s1, "a1",a1, "r",r, "sprime", sprime, "q s1 a1", self.Q[s1][a1], "aprimeq", aprimeq)
            print('alphadelta', alphadelta)
        trace = 1   
        i = 0
        while trace > 0.01 and i < len(actions): #len(self.recentactions):
            s = senses[i] #self.recentsensations[i]
            a = actions[i] #self.recentactions[i]
            if not s in senses[0:i]: #i+1:]: #self.recentsensations[i+1:]: #[0:i]:  #[i+1:]: # [0:i]s doesn't occur again in the list of recent sensations
                oldq = self.Q[s][a]
                self.Q[s][a] += alphadelta * trace
                if debugmode():
                    print("updating s", s , "a", a, "old", oldq, "new",self.Q[s][a], "trace", trace)
                if abs(self.Q[s][a] - oldq) > changeDiff:
                    self.agentchangestate(s)
            trace = trace * self.gamma * self.agentlambda
            i += 1

class QlambdaGridAgent(GridAgent):
    def agentLearn (self, s1, a1, r, sprime):    # Q(lambda), replace traces
        global changeDiff
        trace = 1
        i = 0
        if debugmode():
            print("states", self.recentsensations)
            print("actions", self.recentactions)
        alphadelta = self.alpha * (r + \
                                        (self.gamma * self.statevalue(sprime)) \
                                        - self.Q[s1][a1])
        while trace > 0.01 and i < len(self.recentactions):
            s = self.recentsensations[i]
            a = self.recentactions[i]
            if not s in self.recentsensations[0:i]:  #[i+1:]: # [0:i]s doesn't occur again in the list of recent sensations
                oldq = self.Q[s][a]
                self.Q[s][a] += alphadelta * trace
                if abs(self.Q[s][a] - oldq) > changeDiff:
                    self.agentchangestate(s)
            trace = trace * self.gamma * self.agentlambda
            i += 1

class QonestepGridAgent(GridAgent):
    def agentLearn (self, s, a, r, sprime):    # onestep qLearning
        oldq = self.Q[s][a]
        delta = (r + (self.gamma * self.statevalue(sprime)) - self.Q[s][a])
        self.Q[s][a] += self.alpha * delta
        if abs(self.Q[s][a] - oldq) > changeDiff:
            self.agentchangestate(s)

### Forward Models

class DeterministicForwardModel:
    def __init__(self, numactions, numstates, initialvalue=0.1):
        self.numactions = numactions
        self.numstates = numstates
        self.initialvalue = initialvalue

    def agentInit(self):
        self.predictednextstate = [[None for i in range(self.numactions)] \
                                   for j in range(self.numstates)]
        self.predictedreward = [[None for i in range(self.numactions)] \
                                   for j in range(self.numstates)]
        self.savedpredictednextstate = [[None for i in range(self.numactions)] \
                                   for j in range(self.numstates)]
        self.savedpredictedreward = [[None for i in range(self.numactions)] \
                                   for j in range(self.numstates)]
        self.q = [[self.initialvalue for i in range(self.numactions)] \
                                   for j in range(self.numstates)]

    def learnworldmodel (self, x, a, y, r):
        self.setpredictednextstate(x, a, y)
        self.setpredictedreward(x, a, r)

    def setpredictednextstate (self, x, a, y):
        self.predictednextstate[x][a] = y

    def setpredictedreward (self, x, a, r):
        self.predictedreward[x][a] = r

    def getpredictednextstate (self, x, a):
        return self.predictednextstate[x][a]

    def getpredictedreward (self, x, a):
        return self.predictedreward[x][a]

def setupEmptyGridModel (sim):
    agent = sim.agent
    saveModel(agent)
    for x in range(agent.numstates):
        for a in range(agent.numactions):
            agent.setpredictednextstate(x, a, sim.env.neighboringSquare(x, a))
            agent.setpredictedreward(x, a, 0)

def revealGoalLocation (sim):
    agent = sim.agent
    env = sim.env
    for x in range(agent.numstates):
        for a in range(agent.numactions):
            s = env.neighboringSquare(x, a)
            if s == env.goalsquare:
                agent.setpredictedreward(x, a, 1)
                agent.setpredictednextstate(x, a, 'terminal')

def setupAccurateModel (sim):
    agent = sim.agent
    saveModel(agent)
    for x in range(agent.numstates):
        for a in range(agent.numactions):
            sp = sim.env.gridworldnextstate(x, a)
            agent.setpredictednextstate(x, a, sp)
            if sp == 'terminal':
                r = 1
            else:
                r = 0
            agent.setpredictedreward(x, a, r)

def setupNullModel (sim):
    agent = sim.agent
    saveModel(agent)
    for x in range(agent.numstates):
        for a in range(agent.numactions):
            agent.setpredictednextstate(x, a, None)   # 0 ?

def setupStayModel (agent):
    saveModel(agent)
    for x in range(agent.numstates):
        for a in range(agent.numactions):
            agent.setpredictednextstate(x, a, x)
            agent.setpredictedreward(x, a, 0)

def saveModel (agent):
    for s in range(agent.numstates):
        for a in range(agent.numactions):
            agent.savedpredictednextstate[s][a] = agent.predictednextstate[s][a]
            agent.savedpredictedreward[s][a] = agent.predictedreward[s][a]

def saveModelAndQ (agent):
    saveModel(agent)
    saveQ(agent)

def restoreModelAndQ (agent):
    restoreModel(agent)
    restoreQ(agent)

def restoreModel (agent):
    for s in range(agent.numstates):
        for a in range(agent.numactions):
            agent.predictednextstate[s][a] = agent.savedpredictednextstate[s][a]

def qLearn (agent, s, a, sprime, r):
    if r == None:
        r = 0
    agent.Q[s][a] += agent.alpha * \
                     (r + (agent.gamma * agent.statevalue(sprime)) \
                        - agent.Q[s][a])

class DynaGridAgent (DeterministicForwardModel, GridAgent):

    def __init__(self, numactions, numstates, epsilon=0.05, alpha=0.5, \
                 gamma=.9, initialvalue=0.1, agentlambda=0.8, expbonus=0.0): #.0001
        GridAgent.__init__(self, numactions, numstates, epsilon, alpha, \
                           gamma, initialvalue, agentlambda)
        self.agenttime = 0
        self.nummodelsteps = 20
        self.explorationbonus = expbonus
        # num states and numactions should be set by call to DynaGridAgent
        self.Q = [[self.initialvalue for i in range(self.numactions)] \
                  for j in range(self.numstates)]
        self.savedQ = [[self.initialvalue for i in range(self.numactions)] \
                       for j in range(self.numstates)]
        self.predictednextstate = [[None for i in range(self.numactions)] \
                                    for j in range(self.numstates)]
        self.predictedreward = [[None for i in range(self.numactions)] \
                                for j in range(self.numstates)]
        self.savedpredictednextstate = [[None for i in range(self.numactions)] \
                                    for j in range(self.numstates)]
        self.savedpredictedreward = [[None for i in range(self.numactions)] \
                                for j in range(self.numstates)]
        self.changedstates = list(range(self.numstates))
        #self.agentInit()

    def agentInit(self):
        self.timeoflasttry = [[0 for i in range(self.numactions)] \
                              for j in range(self.numstates)]
        setupStayModel(self)  

    def learnworldmodel(self, x, a, y, r):
        DeterministicForwardModel.learnworldmodel(self, x, a, y, r)
        self.agenttime += 1
        self.timeoflasttry[x][a] = self.agenttime

    
    def agentLearn (self, s, a, reward, sprime):       # onestep dyna
        global changeDiff
        qLearn(self, s, a, sprime, reward)
        self.learnworldmodel(s, a, sprime, reward)
        for i in range(self.nummodelsteps):
            for j in range(10 * self.nummodelsteps):
                s = randrange(self.numstates)
                a = randrange(self.numactions)
                sp = self.getpredictednextstate(s, a)
                r = self.getpredictedreward(s, a)
                if r == None:
                    r = 0
                if sp != None and sp != s:  # sp != s added
                    oldq = self.Q[s][a]
                    qLearn(self, s, a, sp, \
                           (r + (self.explorationbonus * \
                                 sqrt(self.agenttime - self.timeoflasttry[s][a]))))
                    if abs(self.Q[s][a] - oldq) >= changeDiff:
                        self.agentchangestate(s)
                    break

class ReducedDynaGridAgent (DynaGridAgent):
    
    def __init__(self, numactions, numstates, epsilon=0.05, alpha=0.5, \
                 gamma=.9, initialvalue=0.1, agentlambda=0.0, expbonus=0.0):
        DynaGridAgent.__init__(self, numactions, numstates, epsilon, alpha, \
                           gamma, initialvalue, agentlambda, expbonus)
        self.nummodelsteps = 0

class PreloadedDynaGridAgent (DynaGridAgent):
     
    def __init__(self, numactions, numstates, epsilon=0.05, alpha=0.5, \
                 gamma=.9, initialvalue=0.1, agentlambda=0.0, expbonus=0.0):
        DynaGridAgent.__init__(self, numactions, numstates, epsilon, alpha, \
                           gamma, initialvalue, agentlambda, expbonus)
        self.nummodelsteps = 1000

    def agentInit(self):
        self.timeoflasttry = [[0 for i in range(self.numactions)] \
                              for j in range(self.numstates)]
        setupAccurateModel(self.sim)

def changeAgentLearnMethod (sim, newlearn):
    env = sim.env
    # also need to reset agent before using new method
    print("Setting up agent with new learning method:", newlearn)
    newagent = None
    if newlearn == 'qlambdareplace':                  # Q(lambda), replace traces
        newagent = QlambdaGridAgent(env.numactions(), env.numstates())
    elif newlearn == 'onestepq':                      # one step Q learner
        newagent = QonestepGridAgent(env.numactions(), env.numstates())
    elif newlearn == 'onestepdyna':                   # one step dyna
        newagent = DynaGridAgent(env.numactions(), env.numstates())
    elif newlearn == 'sarsalambdatraces':             # Sarsa(lambda), replace traces
        newagent = SarsaLambdaGridAgent(env.numactions(), env.numstates())
    elif newlearn == 'sarsa':             # Sarsa(lambda), replace traces
        newagent = SarsaGridAgent(env.numactions(), env.numstates())
    else:
        print("Error: Learning method requested", newlearn, "not implemented")
    if newagent != None:
        sim.agent = newagent
        newagent.sim = sim

def saveQ (agent):
    for s in range(agent.numstates):
        for a in range(agent.numactions):
            agent.savedQ[s][a] = agent.Q[s][a]

def restoreQ (agent):
    for s in range(agent.numstates):
        for a in range(agent.numactions):
            agent.Q[s][a] = agent.savedQ[s][a]

def avi (sim=None):
    global SIM
    if sim == None:
        sim = SIM
    agent = sim.agent
    saveQ(agent)
    keepon = True
    while keepon:
        delta = 0
        for s in range(agent.numstates):
            for a in range(agent.numactions):
                sp = agent.getpredictednextstate(s, a)
                r = agent.getpredictedreward(s, a)
                qtemp = agent.Q[s][a]
                qLearn(agent, s, a, sp, r)
                delta = max(delta, abs(qtemp - agent.Q[s][a]))
        if delta < 0.0001:
            keepon = False
           
## Value Iteration
def vi1 (sim=None):
    global SIM
    if sim == None:
        sim = SIM
    agent = sim.agent
    saveQ(agent)
    for s in range(agent.numstates):
        agent.Q[s][0] = max([agent.savedQ[s][a] for a in range(agent.numactions)])
    saveQ(agent)
    for s in range(agent.numstates):
        values = []
        for a in range(agent.numactions):
            sp = agent.getpredictednextstate(s, a)
            r = agent.getpredictedreward(s, a)
            if r == None:
                r = 0
            if sp == None or sp == 'terminal':
                spq = 0
            else:
                spq = agent.savedQ[sp][0]
            values.append(r + (agent.gamma * spq))
        mx = max(values)
        for a in range(agent.numactions):
            v = values[a]
            if v == mx:
                agent.Q[s][a] = v
            else:
                agent.Q[s][a] = 0
 
def ape (agent=None):
    global AGENT
    if agent == None:
        agent = AGENT
    saveQ(agent)
    delta = 0
    for s in range(agent.numstates):
        for a in range(agent.numactions):
            sp = agent.getpredictednextstate(s, a)
            r = agent.getpredictedreward(s, a)
            qtemp = agent.Q[s][a]
            ap = agent.policy(sp)
            agent.Q[s][a] = r + (agent.gamma * agent.savedQ[sp][ap])
            delta = max(delta, abs(qtemp - agent.Q[s][a]))
    return delta < 0.0001
    

def aperandom(agent=None):
    global AGENT
    if agent == None:
        agent = AGENT
    saveQ(agent)
    delta = 0
    for s in range(agent.numstates):
        for a in range(agent.numactions):
            sp = agent.getpredictednextstate(s, a)
            r = agent.getpredictedreward(s, a)
            qtemp = agent.Q[s][a]
            ap = agent.policy(sp)
            if sp == 'terminal':
                newq = 0
            else:
                newq = 0
                for ap in range(agent.numactions):
                    newq += agent.savedQ[sp][ap]
                newq = float(newq) / agent.numactions
            agent.Q[s][a] = r + (agent.gamma * newq)
            delta = max(delta, abs(qtemp - agent.Q[s][a]))
    return delta < 0.0001

def simcollect (sim, s, a, reward, nextsensation):
    if nextsensation == 'terminal':  # new episode  reset appropriate counters
        sim.episodestepnum = 0
        sim.episodenum += 1
    else:                               # otherwise incr episode step
        sim.episodestepnum +=1
    sim.stepnum += 1

def displayParameters (agent=None):
    "Shows agent's parameters"
    global SIM
    if agent == None:
        agent = SIM.agent
    print("Current agent parameters:")
    if isinstance(agent, QonestepGridAgent):
        print("One step Q grid agent")
    elif isinstance(agent, QlambdaGridAgent):
        print("Q lambda with traces grid agent")
    elif isinstance(agent, DynaGridAgent):
        print("Dyna grid agent")
    elif isinstance(agent, SarsaLambdaGridAgent):
        print("Sarsa lambda grid agent")
    elif isinstance(agent, SarsaGridAgent):
        print("Sarsa grid agent")
    else:
        print("Grid agent is of type", type(agent))
    print("alpha:", agent.alpha, "  gamma:", agent.gamma, "  epsilon:", agent.epsilon)
    if not (isinstance(agent, QonestepGridAgent) or isinstance(agent, SarsaGridAgent)):
        print("lambda:", agent.agentlambda, end="   ")
    print("initial value:", agent.initialvalue)
    if isinstance(agent, DynaGridAgent):
        print("exploration bonus:", agent.explorationbonus, "  num model steps:", agent.nummodelsteps)

def resetParameters (agent=None, alpha=None, gamma=None, epsilon=None, agentlambda=None, \
                     explorationbonus=None, initialvalue=None):
    "Changes agent's parameters"
    global SIM
    if agent == None:
        agent = SIM.agent
    if alpha != None:
        agent.alpha = alpha
    if gamma != None:
        agent.gamma = gamma
    if epsilon != None:
        agent.epsilon = epsilon
    if agentlambda != None:
        agent.agentlambda = agentlambda
    if isinstance(agent, DynaGridAgent):
        if explorationbonus != None:
            agent.explorationbonus = explorationbonus
        if initialvalue != None:
            agent.initialvalue = initialvalue
        #how about num model steps too?

