#<html><body><pre>

# RLinterface module

"""
This module provides a standard interface for computational experiments with 
reinforcement-learning agents and environments. The interface is designed to 
facilitate comparison of different agent designs and their application to different
problems (environments). See http://abee.cs.ualberta.ca:7777/rl-twiki/bin/view/RLAI/RLI5.

Class: RLinterface
     initialize with:   rli = RLinterface(agent, env)
          where  agent and env have the following methods defined:
                 agent.agent_init(taskspec)
                 agent.agent_start(o) -> a   
                 agent.agent_step(r, o) -> a
                 agent.agent_end(r)
                 env.env_init() -> taskspec
                 env.env_start() -> o
                 env.env_step(a) -> r, o
                 env_state() -> state key
                 env_random_seed() -> random seed key
                 optionally env_step can take a state key and a random seed key
Methods:
RL_benchmark() -> performance, standard error
RL_init()
RL_start() -> o, a
RL_step() -> r, o, a
RL_episode() -> o0, a0, r1, o1, a1, ..., rT
RL_total_reward(gamma) - > total gamma discounted reward of current/last episode
RL_num_steps() -> number of steps in current/last episode


"""

class RLinterface:                       #<a name="RLinterface"></a>[<a href="RLdoc.html#RLinterface">Doc</a>]
    """Object associating a reinforcement learning agent with its environment;
    stores next action; see http://rlai.cs.ualberta.ca/RLAI/RLinterface.html."""

    def __init__(self, agent, env):
    	"""Store functions defining agent and environment""" 
    	self.agent = agent   
    	self.environment = env
    	self.numsteps = 0
    	self.rewards = []
    	self.o = 'terminal'                     # force start of new episode
    	self.a = None			        # the action to be used in the next step
    	self.RL_init()

    def RL_init(self):
        """Initialize both the agent and the environment"""
        taskspec = self.environment.env_init()
        self.agent.agent_init(taskspec)

    def RL_start(self):
        """Start an episode """
        self.o = self.environment.env_start()
        self.a = self.agent.agent_start(self.o)
        self.rewards = []
        self.numsteps = 0
        return self.o, self.a

    def RL_step(self):
        """Do one step of the simulation"""
        r, self.o = self.environment.env_step(self.a)
        self.rewards.append(r)
        self.numsteps += 1
        if self.o == 'terminal':
            self.agent.agent_end(r)
            self.a = None
            return [r]
        else:
            self.a = self.agent.agent_step(r, self.o)
            return r, self.o, self.a

    def RL_episode(self):
        """Run the simulation for one episode"""
        obslist = list(self.RL_start())
        while self.o != 'terminal': # max steps test???
            new = self.RL_step()
            obslist.extend(new)
        return obslist

    def RL_total_reward(self,gamma):
        """calculate total discounted reward from current (or last) episode"""
        discount = 1
        tot = 0
        i = len(self.rewards) - 1
        while i >= 0:               # go through rewards from end to start
            tot += self.rewards[i] * discount
            discount *= gamma
            i -= 1
        return tot

    def RL_num_steps(self):
        """returns number of steps so far or in last episode"""
        return self.numsteps
        

#</pre></body></html>
