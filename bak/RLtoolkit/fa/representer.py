
### Representers take their input and represent it.  The input should be an array
### of numbers, or possibly a list of indices of active features.
### The new representation output
### could be either a list of indices indicating which inputs are active or present,
### or an array giving the activity level of all of each input:
###
###   representer.represent(input)
###
### Some representers may be able to adapt to their input distribution.  For this,
### the recommended interfaces are:
###
###   representer.representerLearn(input, weighting)
###   representer.representerLearnLast(input, output, weighting)
###
### The latter is a computationally cheaper version that assumes the last call to
### represent with this representer was given "input" and returned "output".
### Weighting is a scalar used by some representers that indicates the extent of 
### learning that should occur.  A weighting of zero means no learning.  A weighting
### of one means a unit amount of learning about this input.  
###
### The learning done by a representer can be undone by calling (faInit representer).  
### This also redoes any random initialization of the representer.  I.e., it does
### all initialization other allocating memory for the data structures.
###
### The "numinputs" and "numoutputs" of a representer are the dimensionality of
### its input and output respectively.
###
### A simple representer can be made by:
###
###   <representertype>(numinputs=10, numoutputs=1000)
###
### i.e., by giving the number of input variables (10) and output features (1000).
### Fancier representers may require more initialization information of course.
###
### All representers also support an "inputdescriptor" input as a way of providing 
### more information about the input.  E.g.,
###
###   <representertype>(numoutputs=1000,
###                     inputdescriptor=[[0, 1, 5], [0, 100, 10]])
###
### The descriptor is a list of (min max resolution) triples, one per dimension of 
### the input.  The example above specifies a twodimensional input, the first 
### coordinate of which ranges from 0 to 1 and has a resolution of 5, and the second
### coordinate of which ranges from 0 to 100 and has a resolution of 10.  The precise
### meaning of the resolution number depends on the particular representer of course,
### but the general idea is to specify how finely the range of the input is to be
### be split up  how fine a distinction the representer's representation will make.

from .fa import *

### Mix in  CHECKINPUTRANGE and CHECKINPUTDIMENSIONALITY to get your inputs 
### checked automatically.

class CheckInputRange:

    def represent(self, input):
        if not inrangep(input, self.inputdescriptor):
            print("Input", str(input), "out of range", str(self.inputdescriptor))
        else:
            return input

class Representer (CheckInputDimensionality, CheckInputRange):
    "Represents its input in a higher dimensional space; the foundation for all representers"
    
    def __init__(self, numinputs, numoutputs, inputdescriptor=None):
        self.numinputs = numinputs
        self.numoutputs = numoutputs
        self.inputdescriptor = inputdescriptor
        if self.numinputs == None:
            self.numinputs = len(self.inputdescriptor)
 
    def representerLearn (self, input, weighting):
        "The default representerLearn method (suffices for most representers)"
        output = represent(self, input)
        self.representerLearnLast(input, output, weighting)

    def representerLearnLast (self, input, output, weighting):
        "The default learning method for a representer does nothing"
        pass

    def faInit (self):
        pass

    def represent (self, input):
        return input[:]     # return a copy of the input if no better method
        
### The effect of a bias can be added using the REPRESENTERWITHBIAS mixin. 
### This mixin causes the last output dimension to be taken over to serve as the 
### constant input of a bias.  It will always be active.
###
### The representer is given the impression that it has one less output  so look
### out, that could cause strange bugs.  Nevertheless, at the current time it looks
### like the right thing to do because it does not change the real number of outputs.
###
### Remember to place this mixin earlier in the superclass list than the representer 
### itself, so that it is properly recognized as more specific.
###
### The current implementation works only for representers that produce a binary
### list of input indices as their output.

class RepresenterWithBias:
    def __init__(self, biasstrength=1):
        self.biasstrength = biasstrength
        #self.numoutputs -= 1           # I need the last one for the bias

    def represent (self, input):
        pass
        # (cons (numoutputs repr) (callnextmethod)))

def inrangep (input, inputdescriptor):
    i = 0
    ok = True
    for min, max, res in inputdescriptor:
        inputi = input[i]
        if inputi > max or inputi < min:
            ok = False
            break
    return ok

#def represent :before ((repr checkinputdimensionality) (input vector))
#  (when (not (= (numinputs repr) (length input)))
#    (error "Input ~A does not match dimensionality ~A" input (numinputs repr))))

def makeRepresenter (representerClass, limits, numintervals, \
                     numlayers=1, contraction=1.0):
    i = 0
    desc = []
    for lower, upper in limits:
        numinterval = numintervals[i]
        newd = [lower, upper, numinterval]
        desc.append(newd)
    representerClass(*[desc, numlayers, contraction])
  

def makeRepresenters (representerClass, conjunctslist, limits, numintervals, \
                                        numlayers=1, contraction=1.0):
    """Takes a list of sets of input indices and returns a corresponding list of
       correspondingly conjunctive representers.  Numintervals may be
       a fixnum or a list.  Limits gives ranges for all the inputs."""
    n = len(limits)
    if not isinstance(numintervals, (tuple, list)):
        numintervals = [ numintervals for i in range(n)]
    reps = []
    for conjuncts in conjunctslist:
        intervals = []
        for i in range(n):
            if i in conjuncts:
                intervals.append(numintervals[i])
            else:
                intervals.append(1)
        reps.append(makeRepresenter(representerClass, limits, intervals, numlayers, contraction))
    return reps

def combinations (n, k, items=None):
    if items == None:
        items = [i for i in range(n)]
    if k == 0:
        return [[]]
    elif k == n:
        return [items]
    else:
        combo = combinations(n-1, k, items[1:])
        for combination in  combinations(n-1, k-1, items[1:]):
            c = [items[0]] + combination
            combo.append(c)
        return combo

def makeSingletonRepresenters (representerClass, limits, numintervals, \
                                           numlayers=1, contraction=1.0):
    return makeRepresenters(representerClass, combinations(len(limits), 1), \
                     limits, numintervals, numlayers, contraction)

def makeDoubletonRepresenters (representerClass, limits, numintervals, \
                                           numlayers=1, contraction=1.0):
    return makeRepresenters(representerClass, combinations(len(limits), 2), \
                     limits, numintervals, numlayers, contraction)

