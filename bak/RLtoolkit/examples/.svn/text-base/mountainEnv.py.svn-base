# Mountain car environment
#  functions getStats -> steps, episodes, episodesteps
#        and getState -> position, velocity, action       return current globals
# RL interface function is mountainEnv(a=None)
#   use   rli = RLinterface(mountainAgent, mountainEnv)
# initialize with setupEnv()

from math import *
from RLtoolkit.utilities import *

minPosition = -1.2			# Minimum car position
maxPosition = 0.6			# Maximum car position (past goal)
maxVelocity = 0.07			# Maximum velocity of car
goalPosition = 0.5			# Goal position - how to tell we are done
velocity = 0.0
position = 0.0
action = 1
steps = episodesteps = episodes = 0
randomStarts = False
	
def mountainEnv(a=None):
    if a == None:               # start of new episode
        return s0()             # return initial sensation
    else:                   
        s, r = do(a)            # do action
        return s, r             # return new sensation and state
	    
def setupEnv():
    global steps, episodesteps, episodes, velocity, position, action
    velocity = 0.0
    position = 0.0
    action = 1
    steps = episodesteps = episodes = 0

def s0():
    "Returns initial state of mountain car for a new episode"
    global steps, position, velocity, episodes, episodesteps, action 
    #lasts, lastr, action = None, 0, 1
    action = 1
    if steps != 0:
        episodes += 1
    episodesteps = 0
    position, velocity = mCarInit()
    # print "Start of episode, sensation is", position, velocity
    return position, velocity
	
def do(a):
    "Does the specified action and returns a new state and reward"
    global action
    action = a
    p, v = mCarStep(a)			# do the action
    global position, velocity, steps, episodesteps, episodes
    position = p
    velocity = v
    steps += 1
    episodesteps += 1
    r = -1				# get reward (always -1 in MC)
    if mCarGoal(p):			# if we've reached the goal
        sp = 'terminal'		        # set the new state to indicate that
    else:
        sp = (p, v)			# otherwise new state is position and velocity
    # print "New state is", sp, "reward is", r
    return sp, r

def mCarHeight(position):
    return sin(3 * position)
	
def mCarSlope(position):
    return cos(3 * position)
	
def mCarStep(a):
    "Applies the action and calculates the new position and velocity"
    global velocity, position
    oldp, oldv = position, velocity
    if a==0:				        # action is backward thrust
        factor = -1
    elif a == 1:				# action is coast
        factor = 0
    else:					# action is forward thrust
        factor = 1
    velocity = minmax(velocity + (.001 * factor)  + \
                    (-.0025 * mCarSlope(position)), 
                     maxVelocity)
    position += velocity
    position = minmax(position, minPosition, maxPosition)
    if (position == minPosition) and (velocity < 0):
        velocity = 0.0
    return position, velocity
	
def mCarGoal (p):
    "Is the car past the goal?"
    return p >= goalPosition
	
def mCarInit ():
    "Set car to its initial position for an episode"
    global randomStarts
    if randomStarts:
        position = randomInInterval(minPosition, goalPosition)
        velocity = randomInInterval(- maxVelocity, maxVelocity)
    else:
        position = -0.5
        velocity = 0.0
    #print "Initial state is", position, velocity
    return position, velocity

def curStats():
    global steps, episodes, episodesteps
    return steps, episodes, episodesteps

def curState():
    global position, velocity, action
    return position, velocity, action
