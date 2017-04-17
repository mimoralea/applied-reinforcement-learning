### 7. Observable and Partially-Observable States

#### 7.1 Is what we see what it is?

The reinforcement learning methods that we have discussed so far make the assumption that the agent
has perfect sensing capability. That is, the agent is able to perceive the world exactly as the
world is. However, in many environments this is not entirely true. Moreover, in some environments
it is vital to take this uncertainty into account. For example, in many robotics environments, often
our sensor measurements have accuracy within a range. Often, GPS readings can vary from 2 meters to
up to 10 meters. Temperature sensors can be provide reading with %5 error margin. The problem is then
that the methods that we have covered until now are not capable of taking this error into account. This
is because the MDP-based methods have a fundamental assumption, the Markovian assumption. Once this 
assumption no longer holds true, because the state signal is not fully-observable, we enter the 
fields of partially-observable markov decision processes.

#### 7.2 State Estimation

From the robotics world a few methods emerged to deal with sensor errors. These methods use probabilistic
techniques to model the uncertainty in the sensor readings. In fact, these methods are some of the most
commonly used methods today in areas like autonomous vehicles, object tracking, navigation, and many more.
These methods are call Bayesian filters. We will look into one of them, the Kalman Filter on the notebook 
for this lecture.

#### 7.3 Control in Partially-Observable Environments

It is important to note that Bayesian filters do not solve the entire decision-making problem, however, they
do efficiently solve the state estimation problem. POMDPs are very complex, and so if the theory underlying.
However, it is good to mention that there exist extensions to most of the algorithms that we have looked at
so far to solve POMDPs for discrete worlds. These methods however, are inapplicable to many practical
problems in robotics, for instance. There are approximate POMDPs methods that sit in between MDPs and POMDPs
and that are capable of giving sufficiently good approximate answers to POMDPs in a reasonable amount of time.
We will refer you to interesting readings in this area for those looking for more information.

#### 7.4 Exercises

In this lesson we learned that what we see is not always what it is happening in the world. Our perceptions might be
biased, we might not have a 20/20 vision and more importantly we might think we have 20/20 but we might not. For this
reason is important to know that there are other ways of estimating states. In the following Notebook we will look
at a very popular method for state estimation called the Kalman Filter for a very basic problem partially-observable
states problem.

#### 7.5 Further Reading

