import io
import gym
import base64
import tempfile

from IPython.display import HTML
from gym import wrappers

env = gym.make('CartPole-v0')
env = wrappers.Monitor(env, tempfile.gettempdir(), force=True)
for i_episode in range(20):
    observation = env.reset()
    for t in range(100):
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        if done:
            print("Episode finished after {} timesteps".format(t+1))
            break
env.close()
