
### This file contains the definition of the hypercross function approximator,
### a form of randomrepresentation system for continuous valued inputs.
### The hypercrossFA is a good example of an expandedrepresentation function
### approximator (ERFA).  Basically all of the work is done by the ERFA methods.
### The first little bit of code below shows all that is needed here.
### After that is the explanation of the hypercross representer, which is where
### all the real hypercross stuff really occurs.

### Here is an example of making a standard hypercross function approximator
### with a 2dimensional input, 1dimensional output, and an internal representation 
### size of 1000:
###
###     (makehypercrossFA '((0 1 5) (0 1 10)) 1 1000)
###
### The first argument is a standard inputdescriptor specifying (min max resolution)
### for each dimension of the input.  Of course you can also call makeERFA directly,
### specifying a hypercrossrepresenter and finalfa constructed as you would like.

  

### A HYPERCROSSREPRESENTER is a two-stage representer.  The final effect is that
### each feature corresponds to a cross shaped region in the input space.  In other
### words, this is continuous kofN function.  At least k of the N dimensions have
### to be sufficiently close to their ideal or target values.

### The first stage converts to 
### an expanded continuous representation in which each continuous input is converted
### to a set of continous inputs.  These are the "bars" or "stripes" along that input 
### dimension.  Each input dimension is treated separately so far.  These measure the
### degree of match on that dimension.  The degree of match is between 0 and 1.

### The second stage consists of M LTUs, each corresponding to a particular 
### combination of stripes, one from each input dimension.  In effect, these LTUs
### have a +1 weight from their target stripe, and a zero weight to the others.
### If their weighted sum is over a threshold (called k above), they are said to be
### active, else they are inactive.

### When a hypercrossrepresenter is created, the user specifies what inputs will
### look like by providing an inputdescriptor.  For example:

###       (makeinstance 'hypercrossrepresenter :numoutputs 10
###                      :inputdescriptor '((0 100 5) (.1 .9 10)))

### specifies a twodimensional input the first dimension of which goes from 0 to 100
### and should be split into 5 intervals (stripes) and the second dimension of which
### lies bewteen .1 and .9 and is apparently more critical as it should have a  
### resolution of 10 intervals. 

from random import *
from .representer import *
normaldensity0 = normaldensity(0)

class HyperCrossRepresenter (Representer):

    def __init__(self, inputdescriptor, numinputs, percentmatchthreshold=0.6):
        Representer.__init__(self, numinputs, 1, inputdescriptor)
        self.stripeactivities = [0 for i in  range(self.numinputs)] # each dimension's stripe activities
        self.centers = [0 for i in range(self.numinputs)]           # each dimension's stripe centers
        self.width = [0 for i in range(self.numinputs)]            # each dimension's stripe width
        self.resolution = [0 for i in range(self.numinputs)]      # each dimension's resolution
        self.LTUconnections = [[0 for i in self.numinputs] for j in self.numoutputs] # each LTU's connectiosn to stripe activities
        self.beta = percentmatchthreshold                        # thresholds of the LTUs
        self.faInit()

    def faInit (self):
        i = 0
        for min, max, res in self.inputdescriptor:
            self.resolution[i] = res
            striepactivieis[i] = [0 for n in range(res)]
            self.width[i] = (float(max - min) / res - 1.0) / 2.0
            self.centers[i] = [0 for n in range(res)]
            c = min
            for k in range(res):
                self.centers[i][k] = c
                c += 2 * self.width[i]
            i += 1
        for j in range(self.numoutputs):
            for i in range(self.numinputs):
                self.LTUconnections[j][i] = random(self.resolution[i])


    def represent (self, input):
        "Represents the list of continuous inputs as a list of active feature indices"
        global normaldensity0
        for i in range(self.numinputs):
            for k in range(self.resolution[i]):
                stripeactivities[i][k] = \
                            normaldensity((float(input[i] - self.centers[i][k]) / self.width[i]))
        replist = []
        for j in range(self.numoutputs):
            nummatches = 0
            for i in range(self.numinputs):
                index = LTUconnections[j][i]
                nummatches += stripeactivities[i][index]
            if nummatches >= (self.numinputs * self.beta * normaldensity0):
                replist.append(j)
        return replist


class HyperCrossRepresenterWithBias (RepresenterWithBias, HyperCrossRepresenter):
    pass


def makehypercrossFA (inputdescriptor, numoutputs, representationsize, \
                                             finalfa=None, percentmatchthreshold=0.2):
    if finalfa == None:
        if numoutputs == 1:
            finalfa = NormalizedStepAdaline(representationsize)
        else:
            finalfa = NormalizedStepAdalineLayer(representationsize, numoutputs)
    return ERFA(HyperCrossRepresenter(inputdescriptor, representationsize, percentmatchthreshold), \
                finalfa)

def draw2dreceptivefield (context, repr, feature, \
                                    dimensionstovary=[0, 1], inputdescriptor=None):
    if inputdescriptor == None:
        inputdescriptor = repr.inputdescriptor
    black = gColorBlack(context)
    f = dimensionstovary[0]
    firstdescriptor = inputdescriptor[dimensionstovary[0]]
    seconddescriptor = inputdescriptor[dimensionstovary[1]]
    min1, max1, num1 = firstdescriptor
    min2, max2, num2 = seconddescriptor
    numinputs = repr.n #repr.numinputs
    array = [0 for i in range(numinputs)]
    gClear(context)
    gdOutlineRect(context, 0,0,51, 51, black)
    x = min1
    for dx in range(1, 50):
        array[0] = x
        y = min2
        for dy in range(1, 50):
            array[1] = y
            if feature in repr.represent(array):
                gdDrawPoint(context, dx, dy, black)
            y += float(max2 - min2) / 50.0
        x += float(max1 - min1) / 50.0

