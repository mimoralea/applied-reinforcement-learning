
from .fa import *
from .linear import *

class Weight:
    def __init__(self, weightvalue, tov, fromv):
        self.w = weightvalue
        self.tov = tov
        self.fromv = fromv

class SparseLinearFunctionApproximator (FunctionApproximator):

    def __init__(self, numinputs, numoutputs):
        FunctionApproximator.__init__(self, numinputs, numoutputs)
        self.numweights = 0
        self.learningrate = 1
        self.fromweights = [[] for i in range(self.numinputs)] #array of weights FROM each input
        self.toweights = [[] for i in range(self.numoutputs)]  # array of weights TO each output

    def faApproximate(sself, inputs):
        approximation = []
        for input in inputs:
            for w in self.fromweights[input]:
                approximation = incrementsparseapproximation(approximation, w)
        return approximation

    def faLearnLastApproximation (self, inputs, outputl, targetl):
        # First I assure that the outputs and targets lists are sorted !
        outputs = outlputl[:].sort()
        targets = targetl[:].sort()
        # Then work out the deltaweights for each output predicted
        learningrate = self.normalizedlearningrate(inputs)
        errors = []
        outputsleft = outputs
        targetsleft = targets
        while outputsleft != [] or targetsleft != []:
            target = targetsleft[0]
            output, guess = outputsleft[0]
            if target == None or target == []:
                outputsleft.pop()
                errors.append([output, learningrate * (0 - guess)])
            elif output == None or output == [] or target < output:
                targetsleft.pop()
                errors.append([target, learningrate])
            elif output < target:
                outputsleft.pop()
                errors.append([output, learningrate * (0 - guess)])
            elif output == target:
                outputsleft.pop()
                targetsleft.pop()
                errors.append([output, learningrate * (1 - guess)])
        #errors.remove (deleteif #'(lambda (x) (< (cdr x) .1)) errors))
        nerrors = errors
        errors = []
        for e, i in nerrors:
            if not i < .1:
                errors.append([e, i])
        # Now work through each input's weights, comparing with the errors
        for input in inputs:
            weightsleft = self.fromweights(input)
            errorsleft = errors
            lastweightsleft = 'first'
            while errorsleft != []:
                errornum, error = errorsleft[0]
                weight = weightsleft[0]
                if weight == [] or weight == None or errornum < weight.to:
                    errorsleft.pop()
                    addweight(self, input, errornum, error, lastweightsleft)
                    if lastweightsleft == 'first':
                        lastweightsleft = self.fromweights[input]
                        lastweightsleft.pop()
                elif weight.to <= errornum:
                    if lastweightsleft == 'first':
                        lastweightsleft = weightsleft
                        lastweightsleft.pop()
                    weightsleft.pop()
                    if self.weightto[weight] == errornum:
                        errorsleft.pop()
                        weight.w += error
                        
class SparseMadaline (NormalizedStepSize, SparseLinearFunctionApproximator):
    pass


## An approximation is an ordered list of (outputnum , intensity) .

def incrementsparseapproximation (approximation, weight):
    #This does not increment in place  it returns the incremented approximation
    to = weight.to
    lastrest = 'first'
    for i in range(len(approximation)):
        cons = approximation[i]
        outputnum = cons[0]
        if to <= outputnum:
            if to == outputnum:
                cons[1] += weight.w
                return approximation
            elif lastrest == 'first':
                return [[to, weight.w]] + approximation
            else:
                return approximation[:i] + [[to, weight.w]] + approximation[i:]
            break

def addweight (fa, fromw, to, weightvalue, location=None):
    weight = Weight(weightvalue, to, fromw)
    if location == 'first':
        fa.fromweights[fromw] = [weight] + fa.fromweights[fromw]
    elif location == None:  # put in sorted order
        weights = fa.fromweights[fromw]
        lastrest = 'first'
        for i in range(len(weights)):
            w = weights[i]
            if weight.tov > w:
                if lastrest == 'first':
                    fa.fromweights[fromw] = [weight] + fa.fromweights[fromw]
                else:
                    fa.fromweights[fromw] = weights[:i] + [weight] + weights[i:]
            lastrest = 'rest'
    else:  # insert after location
        print("location is ", location, "add after that")
    fa.toweights[to] = [weight] + fa.toweights[to]
    fa.numweights += 1
                





 
