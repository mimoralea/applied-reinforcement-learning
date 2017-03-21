#!/usr/bin/python

import gym
import numpy as np

from gym import wrappers

alpha = 0.9
gamma = 0.9

env = gym.make('Taxi-v1')
q = np.random.random((env.nS, env.action_space.n))
#env = wrappers.Monitor(env, '/tmp/taxi-v1', force=True)

def exploration(episode):
    return 0.5 if episode < 10000 else 0.999

for episode in range(1000000):
    state = env.reset()

    while True:
        if np.random.random() > exploration(episode):
            action = env.action_space.sample()
        else:
            action = np.argmax(q[state])
        nstate, reward, done, _ = env.step(action)
        if done:
            q[state][action] = q[state][action] + alpha * (reward - q[state][action])
            break
        else:
            q[state][action] = q[state][action] + alpha * (reward + gamma * q[nstate].max() - q[state][action])
        state = nstate
        #env.render()

for i in range(len(q)):
    for j in range(len(q[i])):
        print('Q(' + str(i) + ',' + str(j) + ');' + str(q[i][j]))

print(q[460][5])
print(q[119][5])
print(q[292][1])
print(q[8][5])
