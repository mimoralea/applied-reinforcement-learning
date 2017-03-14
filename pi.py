import numpy as np
import pprint
import json
import sys

def policy_evaluation(policy, env, discount_factor=.75, theta=0.000001):
    V = np.zeros(env.nS)
    # print('evaluating policy')
    while True:
        delta = 0
        # For each state, perform a "full backup"
        for s in range(env.nS):
            v = 0
            # Look at the possible next actions
            for a, action_prob in enumerate(policy[s]):
                # For each action, look at the possible next states...
                for  prob, next_state, reward, done in env.P[s][a]:
                    # Calculate the expected value
                    v += action_prob * prob * (reward + discount_factor * V[next_state] * (not done))
                    # print(s, a, prob, next_state, reward, done, v)
            # How much our value function changed (across any states)
            delta = max(delta, np.abs(v - V[s]))
            # print(delta)
            V[s] = v
        # Stop evaluating once our value function change is below a threshold
        if delta < theta:
            break
    return np.array(V)

def policy_improvement(env, policy_eval_fn=policy_evaluation, discount_factor=0.75):
    # Start with a random policy
    policy = np.ones([env.nS, env.nA]) / env.nA

    iterations = 0
    while True:
        # Evaluate the current policy
        V = policy_eval_fn(policy, env, discount_factor)
        iterations += 1
        # Will be set to false if we make any changes to the policy
        policy_stable = True
        # For each state...
        for s in range(env.nS):
            # The best action we would take under the currect policy
            chosen_a = np.argmax(policy[s])

            # Find the best action by one-step lookahead
            # Ties are resolved arbitarily
            action_values = np.zeros(env.nA)
            for a in range(env.nA):
                for prob, next_state, reward, done in env.P[s][a]:
                    action_values[a] += prob * (reward + discount_factor * V[next_state])
            best_a = np.argmax(action_values)

            # Greedily update the policy
            if chosen_a != best_a:
                policy_stable = False
            policy[s] = np.eye(env.nA)[best_a]

        # If the policy is stable we've found an optimal policy. Return it
        if policy_stable:
            return policy, V, iterations

class Env:
    def __init__(self):
        self.nS = 30
        self.nA = 2
        self.P = np.zeros((self.nS, self.nA), dtype=np.ndarray)

filename=sys.argv[1]

with open(filename) as data_file:
    data = json.load(data_file)

env = Env()
# for  prob, next_state, reward, done in env.P[s][a]:
for state in data['states']:
    for action in state['actions']:
        #print(state['id'], action['id'])
        trans = []
        for transition in action['transitions']:
            trans.append((transition['probability'], transition['to'],
                          transition['reward'],
                          #True if state['id'] == 29 else False))
                          False))
        env.P[state['id']][action['id']] = trans

for si in range(30):
    for ai in range(2):
        # print('for state, action pair ', si, ai)
        pass

print('running policy improvement')
policy, v, it = policy_improvement(env)
print("Policy Probability Distribution:")
print(policy)
print("")

print("Value Function:")
print(v)
print("")

print("Number Iterations:")
print(it)
print("")
