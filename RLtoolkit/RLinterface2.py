#<html><body><pre>

# RLinterface module

"""
This module provides a standard interface for computational experiments with 
reinforcement-learning agents and environments. The interface is designed to 
facilitate comparison of different agent designs and their application to different
problems (environments). See http://abee.cs.ualberta.ca:7777/rl-twiki/bin/view/RLAI/RLI5.

Class: RLinterface
     initialize with:   rli = RLinterface(agentFunction, envFunction)
          where  agentStartFunction(s) -> a   
                 agentStepFunction(s, r) -> a
                 envStartFunction() -> s
                 envStepFunction(a) -> s, r
Methods:
step() --> r, s, a
steps(numSteps) --> r, s, a, r, s, a, r, s, a, ...
episode([maxSteps]) --> s0, a0, r1, s1, a1, ..., rT, 'terminal'
episodes(num, maxSteps [,maxStepsTotal]) --> s0, a0, r1, s1, a1, ..., rT, 'terminal', s0, a0 ...
stepsQ(numSteps) like steps but no returned value (quicker and quieter)
episodeQ([maxSteps]) like episode but no returned value (quicker and quieter)
episodesQ(num, maxSteps [,maxTotal]) like episodes but no returned value (quicker and quieter)

"""

class RLinterface:                       #<a name="RLinterface"></a>[<a href="RLdoc.html#RLinterface">Doc</a>]
    """Object associating a reinforcement learning agent with its environment;
    stores next action; see http://rlai.cs.ualberta.ca/RLAI/RLinterface.html."""

    def __init__(self, agentStartFn, agentStepFn, envStartFn, envStepFn):
    	"""Store functions defining agent and environment""" 
    	self.agentStartFunction = agentStartFn	    
    	self.environmentStartFunction = envStartFn      
    	self.agentStepFunction = agentStepFn
    	self.environmentStepFunction = envStepFn
    	self.s = 'terminal'                     # force start of new episode
    	self.action = None			# the action to be used in the next step

 
    def step (self):                #<a name="step"></a>[<a href="RLdoc.html#step">Doc</a>]
        """Run one step; this is the core function, used by all the others in RLinterface module."""
        if self.s == 'terminal':			# first step of an episode
            return self.startEpisode()
        else:
            return self.stepnext()
                       
    def stepnext (self):                #<a name="stepnext"></a>[<a href="RLdoc.html#stepnext">Doc</a>]
        """Run one step which is not a first step in an episode."""
        self.s, r = self.environmentStepFunction(self.action)
        self.action = self.agentStepFunction(self.s, r)
        if self.s == 'terminal':		# last step of an episode
            return r, self.s                        # no action but agent learned
        else:       		                # regular step
            return r, self.s, self.action           # action and learning

    def steps (self, numSteps):             #<a name="steps"></a>[<a href="RLdoc.html#steps">Doc</a>]
        """Run for numSteps steps, regardless of episode endings.
        return the sequence of sensations, rewards and actions."""
        oaseq = []
        for step in range(numSteps):		# run for numSteps steps
            new = self.step()
            oaseq.extend(new)
        return oaseq

    def startEpisode(self):
        "Call the environment and agent start functions"
        self.s = self.environmentStartFunction()
        self.action = self.agentStartFunction(self.s)
        return [self.s, self.action]
            
    def episode (self, maxSteps=1000000):   #<a name="episode"></a>[<a href="RLdoc.html#episode">Doc</a>]
        """Run for one episode, to a maximum of maxSteps steps, and return the episode."""
        oaseq = self.startEpisode()
        step = 1
        while self.s != 'terminal' and step < maxSteps:  #stop at end of episode or maxsteps
            new = self.stepnext()
            oaseq.extend(new)
            step += 1
        return oaseq

    def episodes (self, numEpisodes, maxSteps=1000000, maxStepsTotal=1000000):  #<a name="episodes"></a>[<a href="RLdoc.html#episodes">Doc</a>]
        """Generate numEpisodes episodes, each no more than maxSteps steps, 
        with no more than maxStepsTotal total; return episodesin one sequence."""
        totsteps = 0
        oaseq = []
        episodeNum = 0
        while episodeNum < numEpisodes and totsteps < maxStepsTotal:	# run for numEpisodes episodes
            oaseq = self.startEpisode() 	    # start new episode
            steps = 1
            totsteps += 1
            episodeNum += 1
            while self.s != 'terminal' and \
                  steps < maxSteps and totsteps < maxStepsTotal: # stop at end or too many steps
                new = self.stepnext()
                oaseq.extend(new)
                totsteps +=1
                steps += 1
        return oaseq

    def stepsQ (self, numSteps):        #<a name="stepsQ"></a>[<a href="RLdoc.html#stepsQ">Doc</a>]
        """Same as steps but quicker, quieter, and returns nothing."""
        for step in range(numSteps):		    # run for numSteps steps
            self.step()
            
    def episodeQ (self, maxSteps=1000000):  #<a name="episodeQ"></a>[<a href="RLdoc.html#episodeQ">Doc</a>]
        """Same as episode but quicker, quieter, and returns nothing."""
        self.startEpisode()
        step = 1
        while self.s != 'terminal' and step < maxSteps:  #stop at end of episode or maxsteps
            self.stepnext()
            step += 1       
            
    def episodesQ (self, numEpisodes, maxSteps=1000000, maxStepsTotal=1000000):  #<a name="episodesQ"></a>[<a href="RLdoc.html#episodesQ">Doc</a>]
        """Same as episodes but quicker, quieter, and returns nothing."""
        totsteps = 0
        episodeNum = 0
        while episodeNum < numEpisodes and totsteps < maxStepsTotal:	# run for numEpisodes episodes
            self.startEpisode() 	    # start new episode
            steps = 1
            totsteps += 1
            episodeNum += 1
            while self.s != 'terminal' and \
                  steps < maxSteps and totsteps < maxStepsTotal: # stop at end or too many steps
                self.stepnext()
                totsteps +=1
                steps += 1

def stepstaken(elist):
    "Returns the number of steps given the list of states, actions and rewards"
    return elist // 3
            
#</pre></body></html>
