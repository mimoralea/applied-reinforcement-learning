# Utilities
import random
from math import *
import operator
from functools import reduce

def minmax (item, limit1, limit2=None):
    "Bounds item to between limit1 and limit2 (or -limit1)"
    if limit2 == None:  #Bound item between - limit1 and + limit1
        return max(-limit1, min(limit1, item))
    else:               #Bound item between limit1 and limit2
        return max(limit1, min(limit2, item))

def frange(start, stop=None, step=1.0):
    """floating point version of range. Returns a list of real numbers starting
    at start, stepping by step, and stopping less than stop.
    If only one number is given, start is assumed to be 0.0, and step to be 1.0"""
    if stop == None:
        stop = start
        start = 0.0
    l = []
    i = float(start)
    while i < stop:
        l.append(i)
        i += step
    return l

def nlist(start, stop=None, step=1):
    if isinstance(start, int):
        return list(range(start, stop, step))
    else:
        return frange(start, stop, step)

def nwithoutm (n, m):
    "Returns a list of 0 to n-1 numbers, with m removed"
    alist = list(range(n))
    alist.remove(m)
    return alist

def factorial (n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)
    
def square (x):             #is this needed?
    if abs(x) > 1e10:
        return 1e20
    else:
        return x*x

def powerOf2 (n):
    lgn = log(n, 2)
    return (lgn - floor(lgn)) == 0

def mod(num, by):
    "mod that works for negative and positive numbers"
    if num >= 0:
        return num % by
    else:
        return (by + (num % by)) % by
    
def printnum(num, total=6, after=2):
    """prints a number with after digits after the decimal point and
    taking up total spaces. Padded on the front if need be"""
    formstr = "%." + str(after) + "f"
    new = formstr%num
    return (total-len(new))*' ' + new

def strlist(alist):
    if isinstance(alist, (tuple, list)):
        return '[' + ', '.join(map(strlist , alist)) + ']'
    elif isinstance(alist, float):
        return str(round(alist, 1))
    elif isinstance(alist, str):
        return "'" + str(alist) + "'"
    else:
        return str(alist)

# List functions

def flatten (l):
    if isinstance(l, (list, tuple)):
        newl = []
        for li in l:
            newl.extend(flatten(li))
        return newl
    else:
        return [l]

def firstn (n, l):
    "Returns a list of the first n elements of l"
    return l[0:n]

def reorderListOfLists(lofl):
    "Makes new list - 1st element is list of all the first elements, 2nd is all the second elements, etc"
    return list(zip(*lofl))

# Policies for an agent to use to choose an action

def randompolicy (numactions):
    "Picks an action based on the random policy"
    return random.randrange(numactions)
	
def egreedy (epsilon, numactions, valuelist):
    "Picks an action based on the epsilon greedy policy"	
    if random.random() < epsilon:
        return randompolicy(numactions)
    else: 
        return argmaxrandom(valuelist)

def argmax (list):
    "Returns an index to the first largest element of the nonnull list; also returns max"
    best_index = 0
    best_value = values[0]
    for i in range(len(values)):
        val = values[i]
        if value > best_value:
            best_value = value
            best_index = index
    return best_index  # do we need to return the value as well?

def argmin (list):
    "Returns an index to the first smallest element of the nonnull list; also returns min"
    best_index = 0
    best_value = values[0]
    for i in range(len(values)):
        val = values[i]
        if value < best_value:
            best_value = value
            best_index = index
    return best_index  # do we need to return the value as well?

def argmaxrandom (values):
    "Returns the index of the maximum entry in the list of values"
    best_index = 0
    best_value = values[0]
    numties = 1
    for i in range(len(values)):
        val = values[i]
        if val < best_value:                        # our older value is better
            pass
        elif val > best_value:                        # the new value is better
            best_index = i
            best_value = val
        else:                                        # there is a tie; randomly pick
            numties += 1
            if random.randrange(0, numties) == 0:        # chose the new one
                best_index = i
                best_value = val
    return best_index                                # old version returned index and value - change?

def argmaxspecial (alist):
    "Returns index to largest in list, breaking ties randomly, or nil if all equal"
    if not reduce(operator.eq, alist):
        bestargs = [0]
        bestvalue = alist[0]
        i = 1
        for value in alist[1:]:
            if value < bestvalue:
                pass
            elif value > bestvalue:
                bestvalue = value
                bestargs = [i]
            elif value == bestvalue:
                bestargs = bestargs + [i]
            i += 1
        arg = bestargs[random.randrange(len(bestargs))]
        return arg, bestvalue
    else:
        return None, None

# Probabilities and Distributions

def randomInInterval(min, max):
    "returns a random number between min and max"
    return min + (random.random() * (max - min))

def randomNormal (randomstate=None):
    if randomstate != None:
        random.setstate(randomstate)
    u = 0.0
    v = 0.0
    while True:
        u = random.random()         # u is bounded (0, 1)
        v = 2.0 * sqrt(2.0) * exp(-0.5) * (random.random() - 0.5) # v is bounded (-max, max)
        if (v * v) <= (-4.0 * u * u * log(u)):
            break
    return v / u
            
def standardizeRandomState (randomstate=None):
    if randomstate == None:
        random.seed(64497)
    else:
        random.setstate(randomstate)
        
def advanceRandomState (numadvances):
    random.jumpahead(numadvances)

def withProbability (p):
    return p > random.random()

def withProb (p1, choice1, choice2):
    "With probability p1, choose choice1, otherwise choice2"
    if random.random() < p1:
        return choice1
    else:
        return choice2

def randomKofN (k, n):
    random.sample(list(range(n)), k)

def randomIntegerOtherThan (n, k):
    "Returns a random integer in [0,n1] that is not k"
    i = random.randrange(n-1)
    if i >= k:
        return i + 1
    else:
        return i
    
def randomExponential (tau):
    return - (tau * log (1 - random.random()))

#stats

def mean (sequence):
    return float(reduce(operator.add, sequence)) / len(sequence)

def mse (target, values):
    return mean([square(v-target) for v in values])

def rmse (target, values):                        #root mean square error
    return sqrt(mse(target, values))

def stdev(l):
    return rmse(mean(l), l)

def stats(l):
    return [mean(l), (stdev(l) / sqrt(len(l)))]

def multistats(lofl):
    return [stats(l) for l in reorderListOfLists(lofl)]

def multimean(lofl):
    return [mean(l) for l in reorderListOfLists(lofl)]

def multimse(target, lofl):
    return [mse(target, l) for l in reorderListOfLists(lofl)]

def multirmse(target, lofl):
    return [rmse(target, l) for l in reorderListOfLists(lofl)]

def multistdev(lofl):
    return [stdev(l) for l in reorderListOfLists(lofl)]

def logistic (s):
    return 1.0 / (1.0 + exp(max(-20, min(20, -s))))
