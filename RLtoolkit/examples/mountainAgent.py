# Mountain car agent -- uses Sarsa learning with replace traces
# (Re)Initialize with mountainEnv.setupAgent()
# Functions for setting agent parameters: setAlpha, setEpsilon
# RL interface function is mountainAgent(s, r=None)
#    e.g. rli = RLinterface(mountainAgent, mountainEnv)

from RLtoolkit.Tiles.tiles import *
from RLtoolkit.traces import *
from RLtoolkit.utilities import *

numTilings = 10				# the number of tilings
posWidth = 1.7 / 8			# tile width for position
velWidth = 0.14 / 8			# tile width for velocity
n = 8192				# number of parameters in theta (mem size)
m = 3					# number of actions (back, coast, forward)
epsilon = 0.01				# probability of random action
alpha = 0.5				# step size parameter
lambd = 0.9				# trace-decay parameter
gamma = 1.0				# discount rate

lasts = None
lasta = 1
lastr = 0
traceH = TraceHolder(n, 0.01, 1000)
F = [[0 for item1 in range(numTilings)] for item2 in range(m)]	# vector of eligibility traces
theta = [0. for item in range(n)]
qValues = [0. for item in range(m)]		    		# array of action values
cTable = CollisionTable(4096, 'safe')  #was 2048

def mountainAgent(s, r=None):
    """Main agent function to send to RLinterface"""
    global lasts, lasta, lastq, traceH, qValues
    if r == None:                       # initialize traces at start of episode
        traceH.decayTraces(0)
        lasts, lastr, lasta = None, 0, 1 
    if s != 'terminal':
        a = choose(s)
        if r !=None:		        # not initial state
            learnSarsa(lasts, lasta, r, s, a)
        lasts, lasta = s, a
        lastq = qValues[a]
        return a
    else:
            return None
        
def setupAgent():
    "(Re)Initialize agent"
    global traceH, F, qValues, theta, lasts, lasta, lastr, cTable
    lasts, lasta, lastr = None, 1, 0
    traceH = TraceHolder(n, 0.01, 1000)
    F = [[0 for item1 in range(numTilings)] for item2 in range(m)]
    qValues = [0.0 for item in range(m)]
    theta = [0.0 for item in range(n)]
    cTable = CollisionTable(4096)
	
def choose (s):
    "Chooses next action"
    global epsilon, m, qValues
    pos, vel = s					# break state up into state vars
    for a in range(m):
        loadFeatures(F, pos, vel, a)			# compute feature sets for new state with a
        qValues[a] = computeQ(a)			# compute action values
    chooseA = egreedy(epsilon, m, qValues)
    # print "Agent chose action", chooseA, "qValues", qValues
    return chooseA

def learnSarsa(lastS, lastA, r, s, a):
    "Learns using sarsa"
    global lastq, alpha, gamma, lambd, numTilings, traceH, F, m, theta, qValues
    # print "learnSarsa", lastS, lastA, r, s, a
    if lastS != None:
        delta = r - lastq
        delta += gamma * qValues[a]
        amt = delta * (alpha / numTilings)
        for i in traceH.getTraceIndices():
            theta[i] += amt * traceH.getTrace(i)
        traceH.decayTraces(gamma * lambd)
        traceH.replaceTraces(F[a])
        #traceH.accumulateTraces(F[a])
        #alist = range(m)
        #alist.remove(a)
        #traceH.replaceTracesZero(F[a], [F[act] for act in alist])
    lastq = qValues[a]
	
def setAlpha(new):
    "reset alpha - works from other modules"
    global alpha
    alpha = new

def setEpsilon(new):
    "reset epsilon - works from other modules"
    global epsilon
    epsilon = new

def computeQ (a):
    "compute value of action for current F and theta"
    q = 0
    for i in F[a]:
        q += theta[i]
    return q
	
def loadFeatures (F, pos, vel, a):
    "Compute feature sets for action at current state"
    global cTable, posWidth, velWidth
    statevars = [pos / posWidth, vel / velWidth]
    loadtiles(F[a], 0, numTilings, cTable, statevars, [a])

def loadF (F, pos, vel):
    "Compute feature sets for each action at current state"
    global m, cTable, posWidth, velWidth
    statevars = [pos / posWidth, vel / velWidth]
    for a in range(m):
        loadtiles(F[a], 0, numTilings, cTable, statevars, [a])
    
def updateTheta (amt):
    for i in traceH.getTraceIndices():
            theta[i] += amt * traceH.getTrace(i)	

