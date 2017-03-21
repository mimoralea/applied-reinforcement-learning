### 
### tilecoder's are a particular kind of ERFA 
###

import RLtoolkit.Tiles.tiles as tiles
from .representer import *
from .ER import *

   
class TileCoderRepresenter (Representer):
    "A basic tilecoder representer"

    def __init__(self, inputdescriptor, numoutputs=8, memorysize=1000, hashingset=None):
        Representer.__init__(self, len(inputdescriptor), numoutputs, inputdescriptor)
        self.memorysize = memorysize
        slist = []
        for min, max, res in self.inputdescriptor:
            slist.append(float(res) / (max - min))
        self.scaling = slist
        self.hashingset = hashingset

    def represent (self, input):
        nlist = []
        i = 0
        for scalingi in self.scaling:
            nlist .append(input[i] * scalingi)
            i += 1
        if self.hashingset == None:
            return tiles.tiles(self.numoutputs, self.memorysize, nlist)
        else:
            return tiles.tiles(self.numoutputs, self.memorysize, nlist, self.hashingset)

def makeTileCoder (inputdescriptor, numoutputs=1, numtilings=8, \
                                         memorysize=1000, hashingset=None):
    representer = TileCoderRepresenter(inputdescriptor, numtilings, memorysize, hashingset)      
    if numoutputs == 1:
        finalfa = NormalizedStepAdaline(memorysize)
    else:
        finalfa = NormalizedStepAdalineLayer(memorysize, numoutputs)
    return ERFA(representer, finalfa)
