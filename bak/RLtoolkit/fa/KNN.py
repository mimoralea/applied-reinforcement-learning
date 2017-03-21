### 
### 
### K-nearest neighbor code
### 
### 

from .fa import *

class KNN (FunctionApproximator):
    "A basic Knearest neighbor function approximator"

    def __init__(self, numinputs, k=1):
        FunctionApproximator.__init__(self, numinputs)
        self.K = k    # neighborhood
        self.datastore = None

    def faApproximate (self, input):
        bestsofar = []
        pairsleft = self.datastore
        while pairsleft != []:
            currentpair = pairsleft[0]
            currentdistance = KNNdistance(input, currentpair[0])
            if len(bestsofar) < self.K:
                bestsofar.append([currentdistance, currentpair])
                bestsofar.sort() # >
            else:
                maxdistancesofar = bestsofar[0][0]
                if currentdistance < maxdistancesofar:
                    bestsofar.pop()
                    bestsofar.append([currentdistance, currentpair])
                    bestsofar.sort()
        return KNNaverage(bestsofar)
    
                                    
    def faLearnLastApproximation (self, input, output, target):
        newarray = input[:]
        self.datastore.append([newarray, target])
        newarray = [0 for i in range(len(input))]

def makeKNN (numinputs, k=1):
    return KNN(numinputs, k) 

def KNNdistance (x, y):
    if not len(x) == len(y):
        10000.0
    else:
        dist = 0.0
        for i in range(len(x)):
            dist += exp((x[i] - y[i]), 2)
    return dist
 
def KNNaverage (l):
    if l == []:
        return 0
    else:
        av = 0.0
        for x in l:
            av += x[1][1]
        return float(av) / len(l)

