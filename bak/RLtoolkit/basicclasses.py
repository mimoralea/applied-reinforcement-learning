class Agent:                                         #[Doc]
    def __init__(self):
        self.agentsim = None
        
class Environment:                                      #[Doc]
    def __init__(self):
        self.envsim = None

class Simulation:                                      #[Doc]
    def __init__(self):
        self.agent = None
        self.env = None
        self.episodenum = 0
        self.episodestepnum = 0
        self.stepnum = 0
        self.rlsim = None
        
debug = False

def debugmode():
    global debug
    return debug

def debugset(value):
    global debug
    debug = value
