
### A multirepresenter is a set of representers that concatenate all the
### representations together to make one big representation.

from .representer import *

class MultiRepresenter (Representer):
    def __init__(self, representers):
        Representer.__init__(self)
        self.representers = representers
        numout = 0
        for r in self.representers:  # should we init each representer?
            numout += r.numoutputs
        self.numoutputs = numout

    def represent (self, input):
        offset = 0
        finalrep = []
        for r in self.representers:
            rep = r.represent(input)
            for c in rep:
                c[0] += offset
            offset += r.numoutputs
            finalrep.append(rep)
        self.representation = rep
        return rep

    def numlayers (self):
        num =0
        for r in self.representers:
            num += r.numlayers
        return num

