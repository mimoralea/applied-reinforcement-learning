import numpy as np
import random
import matplotlib.pylab as pl
import pdb 
import sys
import datetime 
from cvxopt import matrix, solvers

random.seed(0)
np.random.seed(0)
solvers.options["show_progress"] = False
solvers.options['glpk'] = {'msg_lev': 'GLP_MSG_OFF'}  # cvxopt 1.1.8

class Soccer(object):
    def __init__(self, algo):
        self.timestep = 0
        self.gamma = 0.9
        self.alpha0 = self.alpha = 0.15
        self.alpha_min = 1.0e-3
        self.alpha_decay = 0.9999954
        self.max_steps = 1000
        self.actions = ["N", "W", "E", "S", "T"]
        self.action_idx = dict(zip(self.actions, range(len(self.actions))))
        self.action_pairs = ["%s%s" % (i, j) for i in self.actions 
                                             for j in self.actions]
        self.players = ["A", "B"]
        self.opponent = {"A": "B", "B": "A"}
        self.board = [(i, j) for i in range(1, 3) for j in range(1, 5)]
        self.goalx = {"A": 1, "B": 4}

        self.states =  [(t1, t2, bw) for t1 in self.board 
                                     for t2 in self.board 
                                     for bw in self.players 
                                     if t1 != t2] 

        # Dictionary to record Q function over action pairs
        d = dict.fromkeys(self.action_pairs, tuple())
        self.Q = {s: d.copy() for s in self.states}        
        
        for state, avdict in self.Q.items():
            for av in avdict.keys():
                # avdict[av] = (random.random(), random.random())
                avdict[av] = (1.0, 1.0)

        # Dictionary to record Q function over actions
        d_single = dict.fromkeys(self.actions, 0.0)
        self.Q_single = {s: d_single.copy() for s in self.states}

        # Variables to monitor state `s` in the CEQ paper
        self.monitor_state = ((1, 3), (1, 2), "B")        
        self.monitor_obs_max = 1E6
        self.monitor_val = np.zeros((int(self.monitor_obs_max), ))
        self.monitor_timestep = np.zeros((int(self.monitor_obs_max), ))
        self.monitor_obs_cnt = 0

        # Assign the algorithm
        self.algos = {  "friend": self.friend,
                        "foe": self.foe,
                        "ceq": self.ceq,
                        "qlearner": self.qlearner
                    }

        self.vf = self.algos[algo]


    def initialize(self):
        positions = random.sample([(1, 2), (1, 3), (2, 2), (2, 3)], 2)
        self.pos = dict(zip(self.players, positions))     
        self.ball_with = np.random.choice(self.players)        

    def display(self):
        grid = [["--"] * 4, ["--"] * 4]
        for player, pos in self.pos.items():
            i, j = pos
            grid[i - 1][j - 1] = "%s " % player

        i, j = self.pos[self.ball_with]     
        grid[i - 1][j - 1] = "%s*" % self.ball_with

        print "|" + "|".join(grid[0]) + "|\n|" +  "|".join(grid[1]) + "|"

    def allowed(self, next_pos, player, opponent):
        return (next_pos in self.board) and (self.pos[opponent] != next_pos)

    def get_next_pos(self, pos, action):
        if action == "N":
            return (pos[0] - 1, pos[1])

        if action == "W":
            return (pos[0], pos[1] - 1)

        if action == "E":
            return (pos[0], pos[1] + 1)

        if action == "S":
            return (pos[0] + 1, pos[1])

        if action == "T":
            return (pos[0], pos[1])

    def move(self, player, action, opponent):        
        next_pos = self.get_next_pos(self.pos[player], action)            
        
        if self.allowed(next_pos, player, opponent):            
            self.pos[player] = next_pos

        if (next_pos == self.pos[opponent]) and (self.ball_with == player):
            self.ball_with = opponent

    def done(self):
        for player in self.players:
            if (self.ball_with == player) and (self.pos[player][1] in [1, 4]):
                return True, player, self.pos[player]

        return False, None, None

    def get_state(self):
        return tuple((self.pos["A"], self.pos["B"], self.ball_with))


    def get_matrix(self, state):        
        N = len(self.actions)        
        QA = np.zeros((N, N))
        QB = np.zeros((N, N))
        for av, qv in self.Q[state].items():
            i, j = [self.action_idx.get(a) for a in list(av)]
            QA[i, j] = qv[0]
            QB[i, j] = qv[1]        
        return QA, QB

    def foe(self, state, *args):
        N = len(self.actions)
        QA, QB = self.get_matrix(state)
        v1 = np.ones((N, 1))
        v0 = np.zeros((N, 1))
        In = np.eye(N)
        TA = np.hstack((-QA.T, -v1))
        TB = np.hstack((-QB, -v1))
        Z = np.hstack((-In, v0))

        # Numpy arrays
        GA = np.vstack((TA, Z))        
        GB = np.vstack((TB, Z))        
        h = np.zeros((GA.shape[0], 1))
        A = np.vstack((v1, [[0]])).T
        b = np.array([[1.0]])

        # CVXOPT variables
        c = matrix(np.array([0.0, 0.0, 0.0, 0.0, 0.0, 1.0]))
        GA = matrix(GA)
        GB = matrix(GB)
        h = matrix(h)
        A = matrix(A)
        b = matrix(b)

        solA = solvers.lp(c, GA, h, A, b, solver="glpk")
        solB = solvers.lp(c, GB, h, A, b, solver="glpk")
        return -solA["x"][-1], -solB["x"][-1], solA, solB

    def ceq(self, state, *args):
        QA, QB = self.get_matrix(state)
        m, n = QA.shape # m rows, n columns

        # Constraint matrix. Not negated yet.
        G = np.zeros((2 * m * (m - 1), m * m))

        # Process m * (m - 1) rationality constraints for A
        row_num = 0
        for r1 in range(m):
            start_col = start_row = m * r1
            end_col = m * (r1 + 1)
            for r2 in range(m):
                if r1 != r2:            
                    G[row_num, start_col : end_col] = QA[r1, :] - QA[r2, :]
                    row_num += 1

        # Process m * (m - 1) rationality constraints for B        
        for c1 in range(n):
            for c2 in range(n):
                if c1 != c2:
                    Z = np.zeros((m, n))
                    Z[:, c1] = QB[:, c1] - QB[:, c2]
                    G[row_num, :] = Z.flatten()
                    row_num += 1
        
        # Positivity constraints
        G = np.vstack((G, np.eye(m * m)))   
        h = np.zeros((G.shape[0], 1))

        # Equality (normalization) constraint
        A = np.ones((1, m * m))
        b = np.array([[1.0]])

        # Objective function
        Qt = QA + QB
        c = Qt.flatten()

        # CVXOPT variables
        c = matrix(-c)
        G = matrix(-G)
        h = matrix(h)
        A = matrix(A)
        b = matrix(b)

        sol = solvers.lp(c, G, h, A, b, solver=None)
        sig = np.array(sol["x"])
        va = np.sum(sig * QA.flatten())
        vb = np.sum(sig * QB.flatten())        
        return -va, -vb, sol, None

    def qlearner(self, state):
        return max(self.Q_single[state].values())
        

    def friend(self, state):        
        qvals = self.Q[state].values()
        va = max(qvals, key=lambda x: x[0])[0]
        vb = max(qvals, key=lambda x: x[1])[1]
        return va, vb, None, None

         
    def Q_update(self, reward, av, prev_state, next_state):                        
        qa, qb = self.Q[prev_state][av]        
        al = self.alpha
        g = self.gamma
        # vf = self.ceq     
        va, vb, _, _ = self.vf(next_state)            

        qa_update = (1.0 - al) * qa + al * ((1.0 - g) * reward["A"] + g * va)
        qb_update = (1.0 - al) * qb + al * ((1.0 - g) * reward["B"] + g * vb)

        self.Q[prev_state][av] = (qa_update, qb_update)
        self.alpha0 *= self.alpha_decay
        self.alpha = max(self.alpha_min, self.alpha0)

        # Record the monitor state
        if (prev_state == self.monitor_state) \
          and (av == "ST") \
          and (self.monitor_obs_cnt < self.monitor_obs_max):
            # print "qa_update = %0.2f, qb_update = %0.2f" % (qa_update, qb_update)
            self.monitor_val[self.monitor_obs_cnt] = qa_update
            self.monitor_timestep[self.monitor_obs_cnt] = self.timestep
            self.monitor_obs_cnt += 1

    def Q_single_update(self, reward, av, prev_state, next_state):
        action = av[0]
        qa = self.Q_single[prev_state][action]
        al = self.alpha
        g = self.gamma
        va = self.vf(next_state)        
        qa_update = (1.0 - al) * qa + al * ((1.0 - g) * reward["A"] + g * va)
        self.Q[prev_state][action] = qa_update
        self.alpha0 *= self.alpha_decay
        self.alpha = max(self.alpha_min, self.alpha0)        

        # Record the monitor state
        if (prev_state == self.monitor_state) \
          and (action == "T") \
          and (self.monitor_obs_cnt < self.monitor_obs_max):
            self.monitor_val[self.monitor_obs_cnt] = qa_update
            self.monitor_timestep[self.monitor_obs_cnt] = self.timestep
            self.monitor_obs_cnt += 1

    def episode(self):      
        self.initialize()        
        self.isdone = False   
        step = 0

        while (not self.isdone) and (step < self.max_steps):
            step += 1
            self.timestep += 1            
            v_action = np.random.choice(self.actions, 2, replace=True)
            players = np.random.permutation(self.players)            
            reward = dict.fromkeys(self.players, 0)

            prev_state = self.get_state()
            for p, a in zip(players, v_action):
                oppn = self.opponent[p]
                self.move(p, a, oppn)
                isdone, goalee, position = self.done()                
                if isdone:                                        
                    if (position[1] == self.goalx[goalee]):
                        reward = {goalee: 100, self.opponent[goalee]: -100}
                    else:
                        reward = {goalee: -100, self.opponent[goalee]: 100}                    
                    self.isdone = True
                    break

            next_state = self.get_state()
            ad = dict(zip(players, v_action))
            av = "%s%s" % (ad["A"], ad["B"])

            if self.vf == self.qlearner:    
                self.Q_single_update(reward, av, prev_state, next_state)
            else:            
                self.Q_update(reward, av, prev_state, next_state)


if __name__ == "__main__":
    algo = "ceq"
    # algo = "foe"
    # algo = "qlearner"
    # algo = "friend"
    soccer = Soccer(algo)
    N = 200000
    for i in range(N):
        if i % 1000 == 0:
            print "episode = %d" % i
        try:
            soccer.episode()
        except KeyboardInterrupt:
            print "Print program interrupted"
            sys.exit(0)
        except:
            print "Error occured, ignoring this episode"
            raise

    tvals = soccer.monitor_timestep[soccer.monitor_timestep>0.]
    mvals = soccer.monitor_val[soccer.monitor_timestep > 0.]
    dvals = np.abs(mvals[:-1] - mvals[1:])

    # Save data as csv
    ts = soccer.monitor_timestep[soccer.monitor_timestep > 0.0].reshape((-1, 1))
    val = soccer.monitor_val[soccer.monitor_timestep > 0.0].reshape((-1, 1))
    data = np.hstack((ts, val))

    suffix = datetime.datetime.now().strftime("%Y-%m-%d_%H_%m_%S")
    np.savetxt("data_%s.txt" % suffix, data)
