### This file contains definitions for linear or singlecell function approximators.

from .fa import *

class SingleUnitFunctionApproximator (FunctionApproximator):
    "Foundation of all singleunit connectionist function approximators"
    
    def __init__(self, numinputs=1):
        FunctionApproximator.__init__(self, numinputs, 1)
        self.initialweight = 0
        self.weights = [self.initialweight for i in range(self.numinputs)]
        self.learningrate = 1
        self.faInit()

### Note that a threshold or bias is not explicitly provided.  To create the effect 
### of a bias, cause one input always to be active .

    def faInit (self):
        for i in range(self.numinputs):
            self.weights[i] = self.initialweight

class Adaline (SingleUnitFunctionApproximator):
    "An adaptive linear element  the delta rule, WidrowHoff rule"

    def faApproximate (self, input):
        num = 0
        for i in input:
            num += self.weights[i] 
        return num

    def faLearnLastApproximation (self, input, output, target):
        learningrateerror = self.normalizedlearningrate(input) * (target - output)
        for i in input:
            self.weights[i] += learningrateerror
  

class SingleLayerFunctionApproximator (FunctionApproximator):
    "Foundation of all singlelayer function approximators  arrays of single units"

    def __init__(self, numinputs=1, numoutputs=1):
        FunctionApproximator.__init__(self, numinputs, numoutputs)
        self.initialweight = 0
        self.weights = [[self.initialweight for i in range(self.numinputs)] for j in range(self.numoutputs)]
        self.learningrate = 1
        self.faInit()


### Note that a threshold or bias is not explicitly provided.  To create the effect 
### of a bias, cause one input always to be active .

    def faInit (self):
        for j in range(self.numoutputs):
            for i in range(self.numinputs):
                self.weights[j][i] = self.initialweight

class Madaline (SingleLayerFunctionApproximator):

    def faApproximate (self, input):
        faa = 0
        for j in range(self.numoutputs):
            for i in  input:  
                faa += self.weights[j][i] 

    def faLearnLastApproximation (self, input, output, target):
        for j in range(self.numoutputs):
            learningrateerror = self.normalizedlearningrate(input) * (target[j] - output[j])
            for i in input:
                self.weights[j][i] += learningrateerror

class SelectableOutput:

### Sometimes it is useful to have a layer of function approximators which 
### allows you to only train or ask for one of their outputs.  These SELECTABLEOUTPUT
### objects have additional functions:
###
###     fa.faApproximate1(input, outputnumber)
###     fa.faLearn1(input, scalartarget, outputnumber)
###     fa.faLearnLastApproximation1(input, scalaroutput, scalartarget, outputnumber)

    def falearn1 (self, input, scalartarget, outputnumber):
        """The default falearn1 just approximates and learns the approximation.
           Surprisingly, this suffices for almost all function approximators."""
        scalaroutput = self.faApproximate1(input, outputnumber)
        return faLearnLastApproximation1(input, scalaroutput, scalartarget, outputnumber)

class SelectableOutputMadaline (Madaline, SelectableOutput): 

    def faApproximate1 (self, input, outputnumber):
        faa = 0
        for i in input:
            faa += self.weights[outputnumber][i]
        return faa

    def faLearnLastApproximation1 (self, input, scalaroutput, scalartarget, outputnumber):
        learningrateerror = self.normalizedlearningrate(input) * (scalartarget - scalaroutput)
        for i in input:
            self.weights[outputnumber][i] += learningrateerror

class NormalizedStepSize:
        
    def normalizedlearningrate (self, input):
        length = float(len(input))
        if length == 0:
            return 0
        else:
            return self.learningrate / length
        
class NormalizedStepAdaline (NormalizedStepSize, Adaline):
    pass

class NormalizedStepMadaline (NormalizedStepSize, Madaline):
    pass



  

