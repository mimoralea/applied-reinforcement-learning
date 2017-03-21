# Solving as MDP using Value Iteration Algorithm

import gym
import numpy as np

def iterate_value_function(v_inp, q_inp, gamma, env):
    ret = np.zeros(env.nS)
    retq = np.zeros((env.nS, env.nA))

    for sid in range(env.nS):
        temp_v = np.zeros(env.nA)
        for action in range(env.nA):
            for (prob, dst_state, reward, is_final) in env.P[sid][action]:
                if is_final:
                    temp_v[action] = temp_v[action] + prob * (reward)
                else:
                    temp_v[action] = temp_v[action] + prob * (reward + gamma * v_inp[dst_state])
        retq[sid] = temp_v
        ret[sid] = max(temp_v)
    return ret, retq

def build_greedy_policy(v_inp, gamma, env):
    new_policy = np.zeros(env.nS)
    for state_id in range(env.nS):
        profits = np.zeros(env.nA)
        for action in range(env.nA):
            for (prob, dst_state, reward, is_final) in env.P[state_id][action]:
                profits[action] += prob*(reward + gamma*v[dst_state])
        new_policy[state_id] = np.argmax(profits)
    return new_policy


env = gym.make('Taxi-v1')
gamma = 0.9
cum_reward = 0
n_rounds = 1000

v = np.zeros(env.nS)
q = np.zeros((env.nS, env.nA))


for t_rounds in range(n_rounds):
    # init env and value function
    observation = env.reset()
    v = np.zeros(env.nS)
    q = np.zeros((env.nS, env.nA))

    # solve MDP
    for _ in range(200):
        v_old = v.copy()
        q_old = q.copy()
        v, q = iterate_value_function(v, q, gamma, env)
        if np.all(v == v_old):
            break
    policy = build_greedy_policy(v, gamma, env).astype(np.int)

    # apply policy
    for t in range(1000):
        action = policy[observation]
        observation, reward, done, info = env.step(action)
        cum_reward += reward
        if done:
            break
    if t_rounds % 50 == 0 and t_rounds > 0:
        print(cum_reward * 1.0 / (t_rounds + 1))

np.set_printoptions(threshold=np.nan)
print('v states')
print(v.tolist())
print('q values')
print(q.tolist())

for i in range(len(q)):
    if v[i] != q[i].max():
        print('oh oh', i)

for i in range(len(q)):
    for j in range(len(q[i])):
        print('Q(' + str(i) + ',' + str(j) + ');' + str(q[i][j]))

print(q[460][5])
print(q[119][5])
print(q[292][1])
print(q[8][5])

