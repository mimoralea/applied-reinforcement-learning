import pdb
import numpy as np
import matplotlib.pylab as pl
import argparse
import logging
import os
import sys
import time
import random
import gym
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor

# Constants
NOP, LFIRE, MFIRE, RFIRE = range(4)

ACTION_ENCODING = {
    NOP: [0, 0, 0, 1],
    LFIRE: [0, 0, 1, 0],
    MFIRE: [0, 1, 0, 0],
    RFIRE: [1, 0, 0, 0]
}

Nfeatures = 13

class FixedLengthList(object):
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.lst = list()

    def put(self, item):
        if len(self.lst) >= self.maxsize:
            self.lst.pop(0)
        self.lst.append(item)

    def putlist(self, lst):
        for item in lst:
            self.put(item)

    def sample(self, samplesize):        
        return random.sample(self.lst, min(samplesize, len(self.lst)))


class LunarLanderAgent(object):
    def __init__(self):
        self.MAX_PURE_EXPL_EPISODES = 25
        self.REPLAY_MEMORY = 100000
        self.TRAINING_BATCH_SIZE = 32
        self.action_space = [NOP, LFIRE, MFIRE, RFIRE]
        self.Nactions = len(self.action_space)
        self.observations = FixedLengthList(maxsize=self.REPLAY_MEMORY)
        self.gamma = 0.995
        self.eps = 0.99
        self.eps_decay = 0.999
        self.min_eps = 0.1
        self.min_learning_rate = 1e-4
        self.learning_rate_init = 1e-4

        # linear regressor
        self.lm = LinearRegression(fit_intercept=False)
        self.lm.coef_ = np.ones((Nfeatures, ))
        self.lm.intercept_ = 0.0

        # Keep track of average reward
        self.max_avg_reward = -1000.0

        # Support vector regressor
        self.svr = SVR(C=0.01, epsilon=0.2)

        # Decision tree regressor
        self.dtr = DecisionTreeRegressor(max_depth=5)

        # Neural net regressor
        self.snn = MLPRegressor(hidden_layer_sizes=(50, 50),
                                activation="relu",
                                batch_size=self.TRAINING_BATCH_SIZE,
                                max_iter=2,
                                solver="adam",
                                warm_start=True,
                                learning_rate="constant",
                                learning_rate_init=self.learning_rate_init) 

        self.fa = self.snn      

    def set_epsilon(self, r):
        # B = np.log(99.0) / 50.0       
        # if self.max_avg_reward <= 0:
        #     self.eps = max(self.min_eps, self.eps * self.eps_decay)
        # elif 0 < self.max_avg_reward <= 50:
        #     self.eps = 0.4 / (1.0 + np.exp(B * r))

        if self.max_avg_reward <= 0:
            self.eps = max(self.min_eps, self.eps * self.eps_decay)
        elif 0 < self.max_avg_reward <= 50:
            self.eps = 0.1
        elif 50 < self.max_avg_reward <= 100:
            self.eps = 0.05
        elif 100 < self.max_avg_reward <= 150:            
            self.eps = 0.02
        elif 150 < self.max_avg_reward <= 200:
            self.eps = 0.01
        elif self.max_avg_reward > 200:
            self.eps = 0.005        

    def dummy_encode(self, actions_):        
        da = [ACTION_ENCODING[a] for a in actions_]            
        N = len(da)
        return np.array(da)

    def append_action(self, states_, action_):
        action_array = np.array(ACTION_ENCODING[action_]).reshape((1, self.Nactions))
        Nsamples = states_.shape[0]
        action_array_repeat = np.repeat(action_array, Nsamples, axis=0)
        return np.hstack((states_, action_array_repeat))

    def get_targets(self, rewards, next_states, vdone):
        m, p = rewards.shape[0], self.Nactions
        values = np.zeros((m, p))
        try:
            for idx, a in enumerate(self.action_space):
                next_state_actions = self.append_action(next_states, a)        
                values[:, idx] = self.fa.predict(next_state_actions).flatten()
        except:
            pass                    
        dv = self.gamma * values.max(axis=1) * (1.0 - vdone)
        values = rewards + dv.reshape((m, 1))        
        return values.flatten()

    def prepare(self, training_set):
        # pdb.set_trace()
        N = len(training_set)
        ones = np.ones((N, 1))        
        ps = [o["state"] for o in training_set]
        ns = [o["next_state"] for o in training_set]        
        states = np.hstack((ones, ps))
        next_states = np.hstack((ones, ns))
        rewards = np.array([o["reward"] for o in training_set]).reshape((N, 1))
        actions = self.dummy_encode([o["action"] for o in training_set])
        vdone = np.array([o["done"] for o in training_set])
        state_actions = np.hstack((states, actions))
        return state_actions, rewards, next_states, vdone        

    def train(self):
        training_set = self.observations.sample(self.TRAINING_BATCH_SIZE)
        state_actions, rewards, next_states, vdone = self.prepare(training_set)
        targets = self.get_targets(rewards, next_states, vdone)                
        self.fa.partial_fit(state_actions, targets)        

        # self.fa.fit(state_actions, targets)        

    def act(self, state, reward, n_episode, done, avg_reward=None):

        # Record average reward
        if done:
            # self.max_avg_reward = max(self.max_avg_reward, avg_reward)
            self.max_avg_reward = avg_reward
            self.set_epsilon(avg_reward)

        # if done and self.max_avg_reward < 50.0:            
        #     self.eps = max(self.min_eps, self.eps * self.eps_decay)
        # elif done and self.max_avg_reward >= 50:
        #     self.eps = self.min_eps / 10.0

        if n_episode < self.MAX_PURE_EXPL_EPISODES:
            return random.choice(self.action_space)
        else:            
            # Decay the learning rate and train the agent
            self.fa.learning_rate_init = \
                max(self.learning_rate_init / np.sqrt(n_episode + 1 - self.MAX_PURE_EXPL_EPISODES),
                    self.min_learning_rate)
            self.train()                    

            # Epsilon-greedy action choice
            if np.random.random() < self.eps:
                return random.choice(self.action_space)
            else:                
                ones = np.ones((self.Nactions, 1))
                state = state.reshape((1, -1))
                state_rep = np.repeat(state, self.Nactions, axis=0)
                state_actions = np.hstack((ones, 
                                           state_rep, 
                                           self.dummy_encode(self.action_space)))
                action_values = self.fa.predict(state_actions)                
                return np.argmax(action_values)      

def main():
    parser = argparse.ArgumentParser(description=None)
    parser.add_argument('env_id', 
                        nargs='?', 
                        default='LunarLander-v2', 
                        help='Select the environment to run')
    args = parser.parse_args()

    # Call `undo_logger_setup` if you want to undo Gym's logger setup
    # and configure things manually. (The default should be fine most
    # of the time.)
    gym.undo_logger_setup()
    logger = logging.getLogger()
    formatter = logging.Formatter('[%(asctime)s] %(message)s')
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # You can set the level to logging.DEBUG or logging.WARN if you
    # want to change the amount of output.
    logger.setLevel(logging.INFO)

    env = gym.make(args.env_id)

    # You provide the directory to write to (can be an existing
    # directory, including one with existing data -- all monitor files
    # will be namespaced). You can also dump to a tempdir if you'd
    # like: tempfile.mkdtemp().
    outdir = "tmp/lunar_lander_results"
    env.monitor.start(outdir, force=True, seed=0)

    # This declaration must go *after* the monitor call, since the
    # monitor's seeding creates a new action_space instance with the
    # appropriate pseudorandom number generator.
    agent = LunarLanderAgent()

    Nfeatures = 13
    max_episodes = 5000    
    tot_rewards = []

    for episode in range(max_episodes):        
        avg_reward = np.mean(tot_rewards[-100:])
        print "Ep %d, alph=%0.2e, arwd=%0.2f, mrwd=%0.2f, eps=%0.2e" \
            % (episode, agent.fa.learning_rate_init, avg_reward, 
               agent.max_avg_reward, agent.eps)

        reward = episode_reward = 0                
        state = env.reset()

        # Perform an initial training step before the episode start.
        _ = agent.act(state, 0, episode, True, avg_reward)
        
        # Simulate an episode
        done = False
        while not done:
            action = agent.act(state, reward, episode, done, avg_reward)
            obs = {"state": state, "action": action}            
            state, reward, done, _ = env.step(action)            
            obs.update({"next_state": state, "reward": reward, "done": done})
            agent.observations.put(obs)
            episode_reward += reward
        tot_rewards.append(episode_reward)    

    env.monitor.close()
    return tot_rewards

if __name__ == '__main__':
    total_rewards = main()
    with open("lunar_lander_5k.txt", "w") as outf:
        for i, r in enumerate(total_rewards):
            outf.write("%d,%f\n" % (i, r))
          
    pl.plot(total_rewards, "-")
    pl.show()
