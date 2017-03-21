#<html><body><pre>

# RLinterface module

"""
This module provides a standard interface for computational experiments with 
reinforcement-learning agents and environments. The interface is designed to 
facilitate comparison of different agent designs and their application to different
problems (environments). See http://abee.cs.ualberta.ca:7777/rl-twiki/bin/view/RLAI/RLI5.

Class: RLinterface
     initialize with:   rli = RLinterface(agentFunction, envFunction)
          where  agentFunction(s, r) -> a   (r is optional, or may be None)
                 envFunction(a) -> s, r      (a is optional, or may be None)
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
    stores next action; see http://abee.cs.ualberta/ca:7777/rl-twiki/bin/view/RLAI/RLI5."""

    def __init__(self, agentFn, envFn):
    	"""Store functions defining agent and environment""" 
    	self.action = None			# the action to be used in the next step
    	self.agentFunction = agentFn	        # the action is set to None to indicate that	
    	self.environmentFunction = envFn        # the next step will be the first of an episode
 
    def step (self):                #<a name="step"></a>[<a href="RLdoc.html#step">Doc</a>]
        """Run one step; this is the core function, used by all the others in RLinterface module."""
        global state
        if self.action == None:			# first step of an episode
            s = self.environmentFunction()
            self.action = self.agentFunction(s)
            return s, self.action
        else:
            s, r = self.environmentFunction(self.action)
            self.action = self.agentFunction(s, r)
            if s == 'terminal':		        # last step of an episode
                return r, s                     # no action but agent learned
            else:       		        # regular step
                return r, s, self.action        # action and learning

    def steps (self, numSteps):             #<a name="steps"></a>[<a href="RLdoc.html#steps">Doc</a>]
        """Run for numSteps steps, regardless of episode endings.
        return the sequence of sensations, rewards and actions."""
        oaseq = []
        for step in range(numSteps):		# run for numSteps steps
            new = self.step()
            oaseq.extend(new)
        return oaseq
            
    def episode (self, maxSteps=1000000):   #<a name="episode"></a>[<a href="RLdoc.html#episode">Doc</a>]
        """Run for one episode, to a maximum of maxSteps steps, and return the episode."""
        self.action = None			    # start new episode
        oaseq = []
        for step in range(maxSteps):		    # run for up to maxSteps
            new = self.step()
            oaseq.extend(new)
            if self.action == None:		    # stop at end of episode
                break
        return oaseq

    def episodes (self, numEpisodes, maxSteps=1000000, maxStepsTotal=1000000):  #<a name="episodes"></a>[<a href="RLdoc.html#episodes">Doc</a>]
        """Generate numEpisodes episodes, each no more than maxSteps steps, 
        with no more than maxStepsTotal total; return episodesin one sequence."""
        totsteps = 0
        oaseq = []
        for episodeNum in range(numEpisodes):	    # run for numEpisodes episodes
            self.action = None			    # start new episode
            for stepNum in range(maxSteps):	    # stop if >  maxSteps steps/episode
                new = self.step()
                oaseq.extend(new)
                totsteps +=1
                if self.action == None:		    # stop at end of episode
                    break
                if totsteps >= maxStepsTotal:	    # stop episode if reached total steps
                    break
            if totsteps >= maxStepsTotal:	    # stop run if reached total steps
                break
        return oaseq

    def stepsQ (self, numSteps):        #<a name="stepsQ"></a>[<a href="RLdoc.html#stepsQ">Doc</a>]
        """Same as steps but quicker, quieter, and returns nothing."""
        for step in range(numSteps):		    # run for numSteps steps
            self.step()
            
    def episodeQ (self, maxSteps=1000000):  #<a name="episodeQ"></a>[<a href="RLdoc.html#episodeQ">Doc</a>]
        """Same as episode but quicker, quieter, and returns nothing."""
        self.action = None			    # start new episode
        for step in range(maxSteps):		    # run for up to maxSteps
            self.step()
            if self.action == None:		    # stop at end of episode
                break
            
    def episodesQ (self, numEpisodes, maxSteps=1000000, maxStepsTotal=1000000):  #<a name="episodesQ"></a>[<a href="RLdoc.html#episodesQ">Doc</a>]
        """Same as episodes but quicker, quieter, and returns nothing."""
        totsteps = 0
        for episodeNum in range(numEpisodes):	    # run for numEpisodes episodes
            self.action = None			    # start new episode
            for stepNum in range(maxSteps):	    # stop if >  maxSteps steps/episode
                self.step()
                totsteps +=1
                if self.action == None:		    # stop at end of episode
                    break
                if totsteps >= maxStepsTotal:	    # stop episode if reached total steps
                    break
            if totsteps >= maxStepsTotal:	    # stop run if reached total steps
                break
            
#</pre></body></html>
