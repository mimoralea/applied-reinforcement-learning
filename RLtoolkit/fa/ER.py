# -*- coding: utf-8 -*-
### This file contains the base definitions 
### for expandedrepresentation function approximators


from .fa import *
from .representer import *
from .linear import *

class ERFA (FunctionApproximator):
    "The foundation for expandedrepresentation function approximators"
    def __init__(self, representer, finalfa, learningrate=None):
        FunctionApproximator.__init__(self, representer.numinputs)
        self.representer = representer
        self.representation = None
        self.finalfa = finalfa
        if learningrate != None:
            self.learningrate = learningrate

    def learningrate (self):
        return self.finalfa.learningrate

    def setLearningrate (self, newlearningrate):
        self.learningrate = newlearningrate
        self.finalfa.learningrate = newlearningrate

    def faInit (self):
        self.finalfa.faInit()

    def faApproximate (self, input):
        self.representation = self.representer.represent(input)
        return self.finalfa.faApproximate(self.representation)

    def faLearnLastApproximation (self, input, output, target):
        print("learn", input, output, target)
        self.finalfa.faLearnLastApproximation(self.representation, output, target)
        self.representer.representerLearnLast(input, self.representation, 1)


### An efficient ERFA separates the representing and learning functions even
### more than in an ordianry ERFA.  It expects a representation as its input.

class EfficientERFA (ERFA):

    def faApproximate (self, representation):
        return self.finalfa.faApproximate(representation)

    def faLearnLastApproximation (self, representation, output, target):
        self.finalfa.faLearnLastApproximation(representation, output, target)

class SelectableOutputERFA (SelectableOutput, ERFA): 

    def faApproximate1 (self, input, outputnumber):
        self.representation = self.representer.represent(input)
        return self.finalfa.faApproximate1(self.representation, outputnumber)

    def faLearnLastApproximation1 (self, input, scalaroutput, scalartarget, outputnumber):
        self.finalfa.faLearnLastApproximation1(self.representation, \
                    scalaroutput, scalartarget, outputnumber)

class SelectableOutputEfficientERFA (SelectableOutput, EfficientERFA):

    def faApproximate1 (self, representation, outputnumber):
        return self.finalfa.faApproximate1(representation, outputnumber)

    def faLearnLastApproximation1 (self, representation, scalarout, scalartarget, outputnumber):
        self.finalfa.faLearnLastApproximation1(representation, \
                    scalaroutput, scalartarget, outputnumber)
