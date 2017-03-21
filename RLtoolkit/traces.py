# Traces code

# Two kinds of traces are handled here: naive traces, and a more complicated but
# better performing variety where only non zero traces are manipulated.
# The calling sequences for both are the same, so you can easily change your code
# to use the other kind by making the trace a different class.
#
#  Classes:    SimpleTraceHolder  (the simpler version)
#          or     TraceHolder (the more complicated one)
#  Initialize your trace object with 
#                  t = SimpleTraceHolder)[memorySize, ignored, ignored])
#       or        t = TraceHolder(]memorySize, minimumTrace, maximumNumberofTraces])
# The following methods are available for each class:
#      t.getTrace(f) - gets the trace value for feature f
#      t.clearTrace(f) - clears the trace value for feature f
#      t.decayTraces(rate) - decays traces by rate
#      t.setTrace(f, newvalue) - sets the trace for feature f to newvalue
#      t.addToTrace(f, value) - adds value to the trace for feature f
#      t.getTraceindices() - returns a list of trace indices (shorter for the non zero trace version)
#      t.replaceTraces(flist) - replaces traces for features in flist with 1.0
#      t.accumulateTraces(flist) - adds 1.0 to trace for each feature in flist
#        (for the last two, flist may be a list or a single item)
#  Trace Holder also has one additional method:
#      t.increaseMinTrace() - increases the minimum trace by 10%


#        Naive Traces
# Below is the code for working with naive traces where no checking against
# a minimum is done, and no attempt is made to improve the performance 
# by only working with non zero traces.

class SimpleTraceHolder:
    "Object to hold eligibility traces"
    
    def __init__(self, mem=8192, min=0, max=1000):
        "Initializes the trace parameters and arrays"
        self.n = mem                                        # memory size
        self.E = {}
        
    def getTrace (self, f):
        "Gets the value for traces for feature f"
        return self.E.get(f, 0.0)
    
    def clearTrace(self, f):
        "Clears any trace for feature f"
        self.E[f] = 0.0
        
    def decayTraces (self, decayRate):
        "Decays all the (nonzero) traces by decay rate"
        for loc in list(self.E.keys()):
            self.E[loc] = self.E[loc] * decayRate
    
    def setTrace (self, f, newTraceValue):
        "Set the trace for feature f to the given value, which must be positive"
        self.E[f] = newTraceValue
            
    def addToTrace (self, f, newValue):
        "Add the new value to the trace for feature f"
        self.E[f] += newTraceValue
        
    def getTraceIndices (self):
        "Gives a list of trace indexes"
        return list(self.E.keys())
    
    def replaceTraces (self, flist):
        "Replaces traces for the features given"
        if isinstance(flist, (tuple, list)):
            for i in flist:
                self.setTrace(i, 1.0)
        else:
            self.setTrace(flist, 1.0)
            
    def replaceTracesZero (self, flist, olist):
        "Replaces traces for given features with 1, other features's 0"
        for nlist in olist:		    # replace traces for other actions
            for i in nlist:
                self.clearTrace(i)
        for i in flist:
            self.setTrace(i, 1.0)	    # replacing traces for current action

    def accumulateTraces (self, flist):
        "Accumulate traces for the features given"
        if isinstance(flist, (tuple, list)):
            for i in flist:
                self.addToTrace(i, 1.0)     # accumulating traces for current action
        else:
            self.addToTrace(flist, 1.0)
        
#     Efficient Traces
# Below is the code for selectively working only with traces >= minTrace. 
# Other traces are forced to zero.  We keep a list of which traces are nonzero
# so that we can work only with them.  This list is implemented as the array
# "nonZeroTraces" together with its length "numNonZeroTraces".  When a trace 
# falls below minTrace and is forced to zero, we remove it from the list by 
# decrementing numNonZeroTraces and moving the last element into the "hole"
# in nonZeroTraces made by this one that we are removing.  A final complication 
# arises because sometimes we want to clear (set to zero and remove) a trace
# but we don't know its position within the list of nonZeroTraces.  To avoid
# having to search through the list we keep inverse pointers from each trace
# back to its position (if nonzero) in the nonZeroTraces list.  These inverse 
# pointers are in the array "nonZeroTracesInverse".


class TraceHolder (SimpleTraceHolder):
    "Object to hold eligibility traces and special arrays for handling non zero traces"
    
    def __init__(self, mem=8192, minT=0.01, maxN=1000):
        "Initializes the trace parameters and arrays"
        self.n = mem                                    # memory sizet.
        self.maxNonZeroTraces = maxN                    # maximum length of list
        self.minTrace = minT                            # all traces below this are set to 0
        self.E = [0.0 for item in range(self.n)]        # vectory of eligibility traces
        self.numNonZeroTraces = 0                       # current number of non zero traces
        self.nonZeroTraces = [0 for item in range(self.maxNonZeroTraces)]   # vector of non zero traces
        self.nonZeroTracesInverse = [0 for item in range(self.n)]           # vector back to original position

    def getTrace (self, f):
        "Gets the value for traces for feature f"
        return self.E[f]
    
    def clearTrace(self, f):
        "Clears any trace for feature f"
        if self.E[f] != 0:
            self.clearExistentTrace(f, self.nonZeroTracesInverse[f])
        
    def clearExistentTrace(self, f, loc):
        "Clears the trace for feature f at location loc in the list of nonzero traces"
        self.E[f] = 0.0
        self.numNonZeroTraces -= 1
        self.nonZeroTraces[loc] = self.nonZeroTraces[self.numNonZeroTraces]
        self.nonZeroTracesInverse[self.nonZeroTraces[loc]] = loc
    
    def decayTraces (self, decayRate):
        "Decays all the (nonzero) traces by decay rate, removing those below minTrace"
        for loc in range(self.numNonZeroTraces-1, -1, -1):          #go through trace list backwards
            f = self.nonZeroTraces[loc]
            self.E[f] = self.E[f] * decayRate
            if self.E[f] < self.minTrace:
                self.clearExistentTrace(f, loc)
    
    def setTrace (self, f, newTraceValue):
        "Set the trace for feature f to the given value, which must be positive"
        if self.E[f] >= self.minTrace:
            self.E[f] = newTraceValue
        elif self.numNonZeroTraces < self.maxNonZeroTraces:
            self.E[f] = newTraceValue
            self.nonZeroTraces[self.numNonZeroTraces] = f
            self.nonZeroTracesInverse[f] = self.numNonZeroTraces
            self.numNonZeroTraces += 1
        else:
            self.increaseMinTrace()
            self.setTrace(f, newTraceValue)
            
    def addToTrace (self, f, newValue):
        "Add the new value to the trace for feature f"
        if self.E[f] >= self.minTrace:
            self.E[f] += newTraceValue
        elif self.numNonZeroTraces < self.maxNonZeroTraces:
            self.E[f] += newTraceValue
            self.nonZeroTraces[self.numNonZeroTraces] = f
            self.nonZeroTracesInverse[f] = self.numNonZeroTraces
            self.numNonZeroTraces += 1
        else:
            self.IncreaseMinTrace()
            self.AddToTrace(f, newTraceValue)
        
    def increaseMinTrace (self):
        """Try to make room for more traces by incrementing minTrace by 10%, culling
            any traces bewlow the new minimum"""
        self.minTrace += self.minTrace * 0.1
        print("Changing minTrace to", self.minTrace)
        for loc in range(self.numNonZeroTraces - 1, -1, -1):        # go through trace list backwards
            f = self.nonZeroTraces[loc]
            if self.E[f] < self.minTrace:                           # check with new minTrace
                self.clearExistantTrace(f, loc)

    def getTraceIndices (self):
        "Returns a list of only the nonzero trace indices to update Theta with"
        return [self.nonZeroTraces[t] for t in range(self.numNonZeroTraces)]

