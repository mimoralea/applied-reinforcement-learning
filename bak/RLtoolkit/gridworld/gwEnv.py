""" This is gridworld code for use standalone, with or without display onto 
an arbitrary gview, or in conjunction with the standard RL interface.  

The walls are stateaction pairs which leave you in the same square rather
than taking you to your neighboring square.  If there were no walls,
wraparound would occur at the gridworld edges# we start with walls all
around the edges.

The barriers (squares you can't pass into) are overlaid on top of this.

The goal square is a terminal state.
Reward is +1 for reaching the goal, 0 else.
"""

from RLtoolkit.utilities import *
from RLtoolkit.basicclasses import *
from random import *
from math import *
import operator

class Gridworld (Environment):
    def __init__(self, width=8, height=6, startsquare=0, goalsquare=1):
        Environment.__init__(self)
        if width == None:
            width = 8
        if height == None:
            height = 6
        if startsquare == None:
            startsquare = 0
        if goalsquare == None:
            goalsquare = 1
        self.width = width
        self.height = height
        self.numsquares = self.width * self.height
        self.startsquare = startsquare
        self.goalsquare = goalsquare
        self.state = None
        self.barrierp = [False for i in range(self.numsquares)]
        self.wallp = [[False for i in range(4)] for j in range(self.numsquares)]
        for v in range(self.height):    # setup walls at gridworld borders
            self.toggleWall(self.squarefromhv(0, v), 3)
            self.toggleWall(self.squarefromhv(self.width-1, v), 1)
        for h in range(self.width):
            self.toggleWall(self.squarefromhv(h, 0), 0)
            self.toggleWall(self.squarefromhv(h, self.height-1), 2)

    def envstartepisode (self):
        self.state = self.startsquare
        return self.startsquare

    def envstep (self, action):
        self.state = self.gridworldnextstate(self.state, action)
        if self.state == 'terminal':
            reward = 1
        else:
            reward = 0
        return self.state, reward
    
    def numactions (self):
        return 4

    def numstates (self):
        return self.numsquares

    def toggleWall (self, square, action):
        self.wallp[square][action] = not self.wallp[square][action]
    
    def toggleBarrier (self, square):
        self.barrierp[square] = not self.barrierp[square]

    def squareh (self, square):
        return square % self.width

    def squarev (self, square):
        return square // self.width

    def squarefromhv (self, h, v):
        s = v * self.width + h
        return s

    def neighboringSquares (self, square):
        sqs = []
        for i in range(4):
            sqs.append(self.neighboringSquare(square, action))
        return sqs

    def neighboringSquare (self, square, action):
        h = self.squareh(square)
        v = self.squarev(square)
        if action == 0:             # left
            return self.squarefromhv(h, (v-1) % self.height)
        elif action == 1:           # up
            return self.squarefromhv((h+1) % self.width, v)
        elif action == 2:           # right
            return self.squarefromhv(h, (v+1) % self.height)
        else:                       # down
            return self.squarefromhv((h-1) % self.width, v)

    def gridworldnextstate (self, s, a):
        proposednextstate = self.neighboringSquare(s, a)
        if self.barrierp[proposednextstate]:
            return s
        elif self.wallp[s][a]:
            return s
        elif proposednextstate == self.goalsquare:
            return 'terminal'
        else:
            return proposednextstate

    def envfn(self, verbose=False, a=None):
        if a == None:
            s = self.envstartepisode()
            if verbose:
                print("Starting new episode with sensation", s)
            self.state = s
            return s
        else:
            s, r = self.envstep(a)
            if verbose:
                print("Did action", a, "got new sensation", s, "and reward", r)
            if s == 'terminal':
                print("Reached goal in ", self.sim.episodestepnum, "steps")
                #sim = self.sim
                #sim.episodenum += 1
                #sim.episodestepnum = 0
            self.state = s
            return s, r
    
class ObjectGridworld (Gridworld):
    def __init__(self, width=8, height=6, startsquare=0, goalsquare=1):
        Gridworld.__init__(self, width, height, startsquare, goalsquare)
        self.objects = [None for i in range(self.numsquares)]
        
    def envstartepisode (self):
        self.state = self.startsquare
        return self.startsquare

    def envstep (self, action):
        self.state = self.gridworldnextstate(self.state, action)
        if self.state == 'terminal':
            reward = 1
        else:
            reward = 0
            extra = self.objects[self.state]
            if extra != None:
                if isinstance(extra, (list, tuple)):
                    reward += extra[1]
                    if extra[0] == 'consumable':    # remove object - used up
                        self.objects[self.state] = None
                else:               #number reward, treat as permanent
                    reward += extra
        return self.state, reward
    
    def addObject (self, square, value, otype='permanent'):
        self.objects[square] = [otype, value]

    def removeObject (self, square):
        self.objects[square] = None

class GPGridworld (Gridworld):

    def envstartepisode (self):
        randomstart = randrange(self.numsquares)
        while self.barrierp[randomstart]:
            randomstart = randrange(self.numsquares)
        self.state = randomstart
        return randomstart

    def envstep (self, action):
        proposednextstate = self.neighboringSquare(self.state, action)
        if not proposednextstate == self.goalsquare:
            # be nasty and give a random action half the time
            if random() > 0.5:
                action = randomIntegerOtherThan(4, action)
                proposednextstate = self.neighboringSquare(state, action)
        if not (self.barrierp[proposednextstate] or self.wallp[self.state][action]):
            self.state = proposednextstate
        if self.state == self.goalsquare:
            return 'terminal', 1.0     # movement into goal
        elif self.state == proposednextstate:
            return self.state, 0              # regular movement
        else:
            return self.state, -1.0            # movement into wall
