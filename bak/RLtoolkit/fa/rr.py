
from random import *
from .representer import *

class BinaryRandomRepresenter (Representer):
    "Standard RR LTU network for binary inputs"
    def __init__(self, numinputs, numoutputs, inputdescriptor=None):
        Representer.__init__(self, numinputs, numoutputs, inputdescriptor)
        self.beta = 0.6
        v = [[0 for i in range(self.numinputs)] for j in range(self.numoutputs)]  #weights of LTUs                     # weights of the LTUs
        self.faInit()
                                       
    def faInit (self):
        "Initializes binaryrandomrepresenter data structures without recreating them"
        for j in range(self.numoutputs):
            for i in range(self.numinputs):
                self.v[j][i] = randint(2)

    def represent (self, input):
        "Represents the binary input vector as a list of active feature numbers"
        replist = []
        for j in range(self.numoutputs):
            nummatches = 0
            for i in  range(self.numinputs):
                if input[i] == self.v[j][i]:
                    nummatches += 1
            if nummatches >= self.numinputs * self.beta:
                replist.append(j)
        return replist
   

