from .RLinterface2 import RLinterface

def agentChoose(s):
    "Chooses the next action"
    global lasta
    lasta += 1
    #print "Agent chose action", lasta
    return lasta

def agentLearn(s, a, r, sp):
    "Learns from the last action done"
    pass #print "Learning from state", s, "action", a, "reward", r, "next s", sp

def agentStart(s):
    "Return the first action"
    global lasta, lasts
    lasta = 0
    lasts = s
    #print "Agent starting with action", lasta
    return lasta

def agentStep(s, r):
    "Learns and gets the next action"
    global lasts, lasta
    agentLearn(lasts, lasta, r, s)
    lasts = s
    if s != 'terminal':
        return agentChoose(s)

def envStart():
    "Returns the initial state"
    global curstate
    curstate = 0
    #print "Environment initializing state to", curstate
    return curstate

def envStep(a):
    "Does the action and returns the next state and reward"
    global curstate
    curstate += 1
    if curstate == 10:
        curstate = 'terminal'
        r = 1
    else:
        r = 0
    #print "Environment did action", a, "got new state", curstate, "and reward", r
    return curstate, r

rli = RLinterface(agentStart, agentStep, envStart, envStep)
rli.episode()
"""
import profile
def run1():
    for i in range(1000):
        rli.episode()

def run3():
    for i in range(1000):
        rli.episodes(1)


def run2():
    for i in range(1000):
        rli.steps(101)

def run1q():
    for i in range(1000):
        rli.episodeQ()

def run3q():
    for i in range(1000):
        rli.episodesQ(1)


def run2q():
    for i in range(1000):
        rli.stepsQ(101)

def run4():
    rli.episodes(1000)

def run4q():
    rli.episodesQ(1000)


profile.run('run1()')
profile.run('run1q()')
profile.run('run2()')
profile.run('run2q()')
profile.run('run3()')
profile.run('run3q()')
profile.run('run4()')
profile.run('run4q()')
"""

