from .RLinterface3 import RLinterface

class Agent:
        
    def agentChoose(self, s):
        "Chooses the next action"
        self.lasta += 1
        print("Agent chose action", self.lasta)
        return self.lasta

    def agentLearn(self, s, a, r, sp):
        "Learns from the last action done"
        print("Learning from state", s, "action", a, "reward", r, "next s", sp)

    def agent_init(self, taskspec):
        """Initializes agent"""
        print("Initializing agent, taskspec is", taskspec)
        self.lasta = 0
        self.lasts = 0
        
    def agent_start(self, s):
        "Return the first action"
        self.lasta = 0
        self.lasts = s
        print("Agent starting with action", self.lasta)
        return self.lasta

    def agent_step(self, r, s):
        "Learns and gets the next action"
        global lasts, lasta
        self.agentLearn(self.lasts, self.lasta, r, s)
        self.lasts = s
        return self.agentChoose(s)

    def agent_end(self, r):
        "Just learns"
        self.agentLearn(self.lasts, self.lasta, r, 'terminal')

class Environment:

    def env_init(self):
        "initialize environment"
        self.curstate = 0
        return "some taskspec info"

    def env_start(self):
        "Returns the initial state"
        self.curstate = 0
        print("Environment initializing state to", self.curstate)
        return self.curstate

    def env_step(self, a):
        "Does the action and returns the next state and reward"
        self.curstate += 1
        if self.curstate == 10:
            self.curstate = 'terminal'
            r = 1
        else:
            r = 0
        print("Environment did action", a, "got new state", self.curstate, "and reward", r)
        return r, self.curstate
    

myagent = Agent()
myenv = Environment()
rli = RLinterface(myagent, myenv)
#rli.RL_init()
print(rli.RL_episode())
print("reward .9", rli.RL_total_reward(.9))
print("reward 1", rli.RL_total_reward(1))
print("Used", rli.RL_num_steps(), "steps")
"""
import profile
def run1():
    for i in range(1000):
        rli.episode()

def run3():
    for i in range(1000):
        rli.episodes(1)


def run2():
    for i in range(1000):
        rli.steps(101)

def run1q():
    for i in range(1000):
        rli.episodeQ()

def run3q():
    for i in range(1000):
        rli.episodesQ(1)


def run2q():
    for i in range(1000):
        rli.stepsQ(101)

def run4():
    rli.episodes(1000)

def run4q():
    rli.episodesQ(1000)


profile.run('run1()')
profile.run('run1q()')
profile.run('run2()')
profile.run('run2q()')
profile.run('run3()')
profile.run('run3q()')
profile.run('run4()')
profile.run('run4q()')
"""

