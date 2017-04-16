# Applied Reinforcement Learning

This repository will contain a series of lessons about Reinforcement Learning and Decision Making.


# Notebooks Installation

This repository contains Jupyter Notebooks to follow along with the lectures. However, there are several
packages and applications that need to be installed. To make things easier on you, I took a little longer
time to setup a reproducible environment that you can use to follow along.

## Install git

Follow the instructions at (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Install Docker

Follow the instructions at (https://docs.docker.com/engine/getstarted/step_one/#step-2-install-docker)

## Run Notebooks

### TL;DR version

1. `git clone git@github.com:mimoralea/applied-reinforcement-learning.git && cd applied-reinforcement-learning`
2. `docker pull mimoralea/openai-gym:v1`
3. `docker run -it --rm -p 8888:8888 -p 6006:6006 -v $PWD/notebooks/:/mnt/notebooks/ mimoralea/openai-gym:v1`

### A little more detailed version:

1. Clone the repository to a desired location (E.g. `git clone git@github.com:mimoralea/applied-reinforcement-learning.git ~/Projects/applied-reinforcement-learning`)
2. Enter into the repository directory (E.g. `cd ~/Projects/applied-reinforcement-learning`)
3. Either Build yourself or Pull the already built Docker container:  
    3.1. To build it use the following command: `docker build -t mimoralea/openai-gym:v1 .`  
    3.2. To pull it from Docker hub use: `docker pull mimoralea/openai-gym:v1`  
4. Run the container: `docker run -it --rm -p 8888:8888 -p 6006:6006 -v $PWD/notebooks/:/mnt/notebooks/ mimoralea/openai-gym:v1`

#### Open the Notebooks in your browser:

* `http://localhost:8888` (or follow the link that came out of the run command about which will include the token)

#### Open TensorBoard at the following address:

* `http://localhost:6006`

This will help you visualize the Neural Network in the lessons with function approximation.

## Docker Tips

* If you'd like to access a bash session of a running container do:  
** `docker ps` # will show you currently running containers -- note the id of the container you are trying to access  
** `docker exec --user root -it c3fbc82f1b49 /bin/bash` # in this case c3fbc82f1b49 is the id  
* If you'd like to start a new container instance straight into bash (without running Jupyter or TensorBoard)  
** `docker run -it --rm mimoralea/openai-gym:v1 /bin/bash` # this will run the bash session as the Notebook user  
** `docker run --user root -e GRANT_SUDO=yes -it --rm mimoralea/openai-gym:v1 /bin/bash` # this will run the bash session as root  


Table of Contents
=================

  * [Part I: Introduction](#part-i-introduction)
      * [1. Introduction to Decision-Making](#1-introduction-to-decision-making)
        * [1.1 Decision-Making](#11-decision-making)
  * [Part II: Reinforcement Learning and Decision-Making](#part-ii-reinforcement-learning-and-decision-making)
      * [2. Sequential Decisions](#2-sequential-decisions)
        * [2.1 Modeling Decision-Making Problems](#21-modeling-decision-making-problems)
        * [2.2 Solutions Representation](#22-solutions-representation)
        * [2.2 Simple Sequential Problem](#22-simple-sequential-problem)
        * [2.3 Slightly more complex problems](#23-slightly-more-complex-problems)
        * [2.4 Evaluating solutions](#24-evaluating-solutions)
        * [2.5 Improving on solutions](#25-improving-on-solutions)
        * [2.6 Finding Optimal solutions](#26-finding-optimal-solutions)
        * [2.7 Improving on Policy Iteration](#27-improving-on-policy-iteration)
        * [2.8 Exercises](#28-exercises)
      * [3. Deterministic and Stochastic Actions](#3-deterministic-and-stochastic-actions)
        * [3.1 We can't perfectly control the world](#31-we-cant-perfectly-control-the-world)
        * [3.2 Dealing with stochasticity](#32-dealing-with-stochasticity)
        * [3.3 Exercises](#33-exercises)
      * [4. Known and Unknown Environments](#4-known-and-unknown-environments)
        * [4.1 What if we don't have a model of the environment?](#41-what-if-we-dont-have-a-model-of-the-environment)
        * [4.2 The need to explore](#42-the-need-to-explore)
        * [4.3 What to learn?](#43-what-to-learn)
        * [4.4 What to do with what we learn?](#44-what-to-do-with-what-we-learn)
        * [4.5 Adding small randomness to your actions](#45-adding-small-randomness-to-your-actions)
        * [4.6 Exercises](#46-exercises)
  * [Part III: Decision-Making in Hard Problems](#part-iii-decision-making-in-hard-problems)
      * [5. Discrete and Continuous States](#5-discrete-and-continuous-states)
        * [5.xx Exercises](#5xx-exercises)
      * [6. Discrete Actions and Continuous Actions](#6-discrete-actions-and-continuous-actions)
        * [6.xx Exercises](#6xx-exercises)
      * [7. Observable and Partially-Observable States](#7-observable-and-partially-observable-states)
        * [7.xx Exercises](#7xx-exercises)
  * [Part IV: Multiple Decision-Making Agents](#part-iv-multiple-decision-making-agents)
      * [8. Single and Multiple Agents](#8-single-and-multiple-agents)
        * [8.xx Exercises](#8xx-exercises)
      * [9. Cooperative and Adversarial Agents](#9-cooperative-and-adversarial-agents)
        * [9.xx Exercises](#9xx-exercises)
  * [Part V: Human Decision-Making and Beyond](#part-v-human-decision-making-and-beyond)
      * [10. Decision-Making and Humans](#10-decision-making-and-humans)
      * [11. Conclusion](#11-conclusion)
      * [12. References](#12-references)

## Part I: Introduction

### 1. Introduction to Decision-Making

#### 1.1 Decision-Making

Decision-making has captivated human intelligence for many years. Humans have always
wondered what makes us the most intelligent animal in this planet. The fact is that
decision-making could be seen as directly correlated with intelligence. The better
the decisions being made, either by a natural or artificial agent, the more likely we
will perceive that agent as intelligent. Moreover, the level of impact decisions have
are directly or indirectly recognized by our societies. Roles in which decision-making
is a primary responsibility are the most highly regarded in today's workforce. If we
think of prestige and salary for example, leadership roles rate higher than management,
and management rate higher than the rest of the labor force.

Being such an important field, it comes at no surprise that decision-making is studied
under many different names. Economics, Neuroscience, Psychology, Operations Research, Adaptive
Control, Statistics, Optimal Control Theory, and Reinforcement Learning are some of the prominent
fields contributing to the understanding of decision-making. However, if we think a little
deeper most other fields are also concerned with optimal decision-making. They might not
necessarily contribute directly to improving our understanding of how we take optimal
decision, but they do study decision-making apply to a specific trade. For instance,
think journalism. This activity is not concerned with understanding how to take optimal
decisions in general, but it is  definitely interested in learning how to take optimal
decisions in regards to preparing news and writing for newspapers. Under this token, we
can see how fields that study decision-making are a generalization of other fields.

In the following lessons we will explore decision-making in regards to Reinforcement
Learning. As Reinforcement Learning is a descendant of Artificial Intelligence, in the remaining
of this chapter we will briefly touch on Artificial Intelligence and also, being such a related
field, we will look at some basics of probability and statistics. On the rest of this lesson, we
will discuss decision-making when there is only one decision to make. This is perhaps the major
difference between Reinforcement Learning and other related fields. Reinforcement Learning
relaxes this constrain allowing the notion of sequential decision-making.
This sense of interaction with an environment sets Reinforcement Learning apart. In later lessons,
we will continue loosing constrains and presenting more abstract topics related to Reinforcement
Learning. After this lesson, we will explore deterministic and stochastic transitions, know
and unknown environments, discrete and continuous states, discrete and continuous actions,
observable and partially observable states, single and multiple agents, cooperative and
adversarial agents, and finally, we will put everything in the perspective of human
intelligence. I hope you enjoy this work.



## Part II: Reinforcement Learning and Decision-Making

### 2. Sequential Decisions

As mentioned before, Reinforcement Learning introduces the notion of sequential decision-making. This
idea of making a series of decisions forces the agent to take into account future sequences of actions,
states and rewards. In this lesson, we will explore some of the most fundamental aspects of sequential
decision making.

#### 2.1 Modeling Decision-Making Problems

In order to attempt solving a problem, we must be able to represent it in a form that abstracts it
allowing us to work on it. For decision-making problems, we can think of few aspects that are
common to all problems.

First, we need to be able to receive percepts of the world, that is, the agent needs to be able to sense
its environment. The input we get from the environment could directly represent the
true state of the world. However, this is not always true. For example, if we are creating a stock trading
bot, we can think of the current stock price as part of the current state of the world. However, any person
that has purchased stocks knows that the sell and buy price are mere estimates of the true price that the
stock will sell for. For some transactions, this price is not totally accurate. Another example in which this
issue is much easier to understand is in robotics. For example, GPS localization is accurate
within a few meters precision. This amount of noise on the sensor could be the difference between an autonomous
car driving safely or instead getting on an accident with the car on the next lane. The point is that as in
the real world, when we model it, we need to account to the fact that things that we "see" are not
necessarily things that "are". This distinction will come up later, for now, we can will assume that we live
in a perfect world and that our perceptions are a true representation of the state of the world. Another
important fact to clarify is the representation of states must include all necessary history within the state.
In other words, the states should be represented as memory-less. This is known as Markov property and it is
a fundamental assumption to solve decision-making problems of the kinds we will be exploring in these lessons.

Second, all decision-making problems have available actions. For the stock bot we can think
of a few actions, sell, buy, hold. We could also add some special action such as limit sell, limit buy,
options, etc. A robot could have the actions to power a given voltage to a given actuator for a given time. As
we clarified the potential of a percept not exactly representing the state of the world, actions might
not turn with the same outcome every time they are taken. That is, actions are not necessarily deterministic.
For the stock agent example, we can think of the small probability that sending a buy request to the server
returns with a server communication error. That is, the probability of actually executing the action we selected
could be 99.9% certain but there is still a small chance that the action doesn't go through as we intended. This
stochasticity is represented as transition functions. This functions represent the probability of successful transition
when taking an action on a given state. The sum of all transitions for a given state action pair must equal 1.
One thing we need to make clear, however, is that probabilities must always be the same. That is, we might not know
the exact probability of transitioning to a new state giving a current and action, but the value will be the
same regardless. In other words, the model of the world must be stationary.

Third, we also have to introduce a feedback signal so that we can evaluate our decision-making abilities.
Many problems in fields other than Reinforcement Learning represent these are cost signal, Reinforcement Learning
refers to these signals as rewards. On our trading agent, the reward could simply be the profit or loss made
from a single transition, or perhaps we could make our reward signal the difference of total assets before and
after making a transaction. In a robotic task, the reward could be slightly more complex. For example, we could
design an agent that gets positive reward while staying up straight walking. Or maybe it gets a reward signal after
a specific tasks is accomplished. The important part of the reward is that this will ultimate have big influence
on how our agent performs. As we can see, rewards are part of the environment. However, often times we have to design
these reward signal ourselves. Ideally, we are able to identify a natural signal that we are interested in maximizing.

The model representation described above is widely known as Markov Decision Processes (MDP). MDP is a framework
for modeling sequential decision-making problems. An MDP is composed of a tuple (S, A, R, T) in which S is the set
of states, A is the set of actions, R is the reward function mapping a state and action pairs to a numeric value, T is
the transition function mapping the probability of reaching a state to a state an action pair.

We will be using MDPs moving forward, though it is important to mention that MDPs have lots of variants,
Dec-MDP, POMDP, QMDP, AMDP, MC-POMDP, Dec-POMDP, ND-POMDPs, MMDPs are some of the most common ones. They all
represent some type of problem related to MDPs. We will be loosing up the constrains MDP present and generalizing
the representation of decision-making problems as we go.

#### 2.2 Solutions Representation

Now that we have a framework to represent decision-making problems, we need to devise a way of communicating
possible solutions to the problems. The first word that comes to mind when thinking about solutions to
decision-making problems is plan. A plan can be seen as a sequence of steps to accomplish a goal. This is
great, but probably too simplistic. Mike Tyson once said, "Everyone has a plan 'till they get punched in the
mouth." And it is true, we need something more adaptive than just a simple plan. The next step then is to think
of a plan and create conditions that helps us deal with the uncertainty of the environment. This type of planning
is known as conditional planning. Which is basically just a regular plan in which we plan in advanced the
contingencies that may arise. However, if we expand this a bit further we can think of a conditional planning
that takes into account every single possible contingency, even those we haven't thought of. This is call universal
plan or better yet, a policy. In Reinforcement Learning, a policy is a function mapping states to actions which
represent a solution to an MDP. The algorithms that we will be discussing later will directly or indirectly produce
the best possible policy, also called optimal policy. This is important to understand and remember.

#### 2.2 Simple Sequential Problem

Given all of the information above, let's review the simplest problem that we can think of. Let's think of a
the problem of a casino with 2 slot machines. To illustrate some important points better, imagine you enter
slot machine area paying a flat fee. However, you are only allowed to play 100 trials on any of the 2 machines.
Also, the machines pay the amount of $1 or nothing on each pull according to an underlying, fixed and unknown
probability. The Reinforcement Learning problem becomes then, how can I maximize the amount of money I could
get from it. Should you start pulling an arm and stick to it for the 100 trials? Should you instead pull 1
and 1? Should you pull 50 and 50? In other words, what is the best strategy or policy for maximizing all
future rewards?

The difficulty of this problem, also known as the k-Armed Bandit, in this case k=2, is that you need to
simultaneously be able to acquire knowledge of the environment and at the same time harness the knowledge you
have already acquired. This fundamental trade-off between exploration versus exploitation is what makes
decision-making problems hard. You might believe that a particular arm has a fairly high payoff probability;
should you then choose it every time? Should you choose one that you know well in order to gain information
about it's payoff? How about choosing one that you might have good information already but perhaps getting more
would improve your knowledge of the environment?

All of the answers to the questions posed above depend on several factors. For example, if instead of allowing you
100 trials I give you 3, how would your strategy change. Moreover, if I give you an infinite number of trials,
then you really want to put time learning the environment even if doing so gives you sub-optimal results early on.
The knowledge that you gain from the initial exploration will ensure you maximize the expected future rewards long
term.


#### 2.3 Slightly more complex problems

When explaining reinforcement learning, it is very common to show a very basic world to illustrate fundamental
concepts. Let's think of a grid world as in figure below:

<IMAGE GOES HERE>

In this world, the agent starts at 'S'. Reaching the space marked with a 'G' ends the game and gives the agent
a reward of 1. Reaching the space with an 'F' ends the game and gives the agent a reward of -1. The agent is able
to select 4 actions every time, (N, S, E, W). The actions selected has exactly the effect we expect. For example,
N would move the agent one cell up, E to the cell on the right. Unless the agent is attempting to enter a space
marked with an 'X' which is a wall and cannot be entered, and unless the agent is in the left most cell trying to
move left, etc. Which will just bounce the agent back to the cell it took the action from.


#### 2.4 Evaluating solutions

Before we being exploring how to get the best solution to this problem. I'd like us to detour into how do we
know how good is a solution. For example, imagine I give you a policy:

<IMAGE GOES HERE>

Is there a way we can put a number to this policy so we can later rank it?

If we need to use a single number, I think we could all agree that the value of the policy can be defined
as the sum of all rewards that we would get starting on state 'S' and following the policy. This algorithm is
called policy evaluation.

One thing you might be thinking after reading the previous paragraph is, but what happens if a policy gives
lots of rewards early on, a nothing later. And another policy gives no rewards early on but lots of reward later.
Is there a way we can account for our preference to early rewards? The answer is yes. So, instead of using the
sum of all rewards as we mentioned before, we will use the sum of discounted rewards in which each reward at time
`t` will be discounted by a factor, let's call it gamma, `t` times. And so we get that policy evaluation basically
calculates the following equation for all states:

```
Vpi(s) = Epi{r_{t+1} + g*r_{t+2} + g**2*r_{t+3} + ... | St = s}
```

So, we are basically finding the value we would get from each of the states if we followed this policy.
Fair enough.

#### 2.5 Improving on solutions

Now that we know how to come up with a single value for a given policy. The natural question we get is how
to we improve on a policy? If we can devise a way to improve and we know how to evaluate, we should be able
to iterate between evaluation and improvement and get the best policy starting from any random policy. And that
would be very useful.

The core of the question is whether there is an action different than the action we are being suggested by the
policy that would make the value calculate above larger? How about we temporarily select a different action than
that suggested by the policy and then follow the policy as originally suggested. This way we would isolate the
effect of the action on the entire policy. This is actually the basis for an algorithm called policy improvement.

#### 2.6 Finding Optimal solutions

One of the powerful facts about policy improvement is that this way of finding better policies from
a given policy actually guarantees that at least a policy of the same exact quality will be returned or better.
This allows us to think of an algorithm that uses policy evaluation to get the value of a policy and then
policy improvement to try to improve this policy and if the improvement just returns any better policy, just
stop. This algorithm is called policy iteration.

#### 2.7 Improving on Policy Iteration

Policy iteration is great because it guarantees that we will get the very best policy available for a given
MDP. However, sometimes it can take unnecessarily large computation before it comes up with that best policy.
Another way of thinking about this is, would there be a small number delta (E.g. 0.0001) that we would be OK with
accepting as a measure of change on any given state. If there is, then we could just cut the policy evaluation
algorithm short and use the value of states to guide our decision-making. This algorithm is called value iteration.

#### 2.8 Exercises

In this lesson we reviewed ways to solve sequential problems. The following Notebook goes into a little more
detail about the Dynamic Programming way of solving problems. We will look into the Fibonacci sequence problem
and devise few ways for solving it. Recursion, Memoization and Dynamic Programming.

Lesson 2 Notebook.

#### 2.9 Further Readings


### 3. Deterministic and Stochastic Actions

#### 3.1 We can't perfectly control the world

One of the main points in reinforcement learning is that actions are not always deterministic. That is, taking
an action does not imply that the action will affect the world the same way each time. Even if the action is taken
given the exact same environmental conditions, the actions are not always deterministic. In fact, most real-world
problems have some stochasticity attached to it in how the world reacts to the agents' actions. For example, we can
think the stock trading agent taking an action to buy a stock, but encountering network issues along the way and
therefore failing at the transaction. Similarly, for the robotics example, we can imagine how moving a robotic
arm to a given location might be precise within certain range. So the probability of that actions affecting the
environment the same way each time even if given the same exact initial conditions is not total.

#### 3.2 Dealing with stochasticity

The way we account for the fact that the world is stochastic is by using expectation of rewards. For example, when
we calculate the rewards we would obtain for taking an action on a given state, we would take into account the probabilities
of transitioning to every single other new state and multiply this probability by the reward we would obtain. If we
sum all of them, we obtain the expectation.

#### 3.3 Exercises

In this lesson we looked into how the environment can get more complex than we discussed in previous lessons.
However, the same algorithms we presented earlier can help us plan when we have a model of the environment. On
the Notebook below we will implement the algorithms discussed in previous chapter in worlds with deterministic
and stochastic transitions.

Lesson 3 Notebook.

#### 3.4 Further Readings


### 4. Known and Unknown Environments

#### 4.1 What if we don't have a model of the environment?

One of the first things that will come to your head after reviewing the last tutorial is, but what's the point if
we need to have the dynamics of the environment? What if it is such a complex environment that it is just too hard
to model? Or better yet, what if we just don't know the environment? Can we still learn the best actions to take
in order to maximize long term rewards?

And, the answer to that question is of course we can deal with unknown environments. Perhaps, this is the most exciting
aspect of reinforcement learning; agents are capable of, through interaction only, learning the best sequence of actions
to take to maximize long term reward.

#### 4.2 The need to explore

The fact that we do not have a map of the environment puts us in need to explore it. Before, we were given a map or as
it is called in reinforcement learning, a model (MDP), but now, we are just dropped in the middle of a world with no
other guidance than our own experiences. The need for exploration comes with a price. We can no longer take a perfect
sequence of actions that maximize the long term rewards from the very first time. Instead, we are now ensured to, at
least, fail a couple of times trying to understand the environment and attempting to reach better goals each time.

If you think about it, this puts us into a dilemma, as exploration has a cost associated with it, how much is it effective
to pay for it such that the long term rewards are maximized. For example, think about a young person graduating from college
at 20 and getting his/her first job. This person gains goes around in 3-4 different jobs early on, but later when we is 50 and
has accumulated experience in a specific field, it might no longer be beneficial to do a career change. It could be much
more effective to keep exploiting the experience he/she has gained. Even if there exists a possibility for higher reward on some
other field. Potentially, given the time left on his/her career, the price of learning a new set of skills might not benefit
the long term goals.

#### 4.3 What to learn?

There are two ways you could think of interacting with world. At first we could think of the value of taking actions on
given states. For example, we calculate the expectation of taking action 'a' when on state 's', then do the same for all
possible state, action combinations. However, as we saw on previous lessons, if we had a model of the environment, we could
determine the exact best value for each state. So, how about learning the model of the environment and then using some of
algorithms on previous lectures to help us guide our decision making?

It turns out that these two ways are the most fundamental classes of algorithms in reinforcement learning. Model-Free methods
are those algorithms that learn straight the action selection. These methods are incredibly useful as they are
capable of learning best actions without any knowledge of the environment. However, they are very data hungry and it
requires lots of samples to get good results. Practically speaking, we cannot just let a bipedal robot fall 1,000,000 times
just for the sake of gaining experience. On the other side of the spectrum, Model-Based methods learn and use the model
of the environment in order to improve the action selection especially early on. Model-Based methods are much more data
efficient and for this reason they are utilized more frequently on problems involving hardware such as robotics.

#### 4.4 What to do with what we learn?

We saw before that we will have to interact with the environment in order to learn. This obvious way of learning is
called "Online learning". In contrast, however, we could also collect the samples we get from our experience and
use that to further evaluate our actions. Intuitively we can think of how humans learn. When we interact with our
environment, we learn directly from our experiences with it, but also, after we have collected these experiences,
we use our memory to think about it and learn so more of what happened, what we did and how we could improve the
outcome if we are face the same problem again. This way of learning is called "Offline learning", and it is also
used in reinforcement learning.

#### 4.5 Adding small randomness to your actions

Finally, there is some other important point often seen in reinforcement learning. The fact that we learn a good
policy does not imply that such policy should be always followed. What if there is some better actions we could
have taken? How do we ensure we always keep an eye on yet a better policy? In reinforcement learning, there are
two main classes of algorithms that address ways of learning while constantly striving for finding better policies.
One ways is called off-policy, and it basically means that the actions taken by the agent are not necessarily always
those that we have determined as the best actions. We would then be updating the values of a policy as if we were
taking the actions of that policy, when in fact we selected the action from another policy. We can also see off-policy
as having two different policies, one that determines the actions that we are selecting, and the other the one that
we use to evaluate our action selection. Conversely, we also have on-policy learning in which we learn and act on
top of the same policy. That is, we evaluate and follow the actions from the same policy.

#### 4.6 Exercises

In this lesson we learned the difference between planning and reinforcement learning. We compared two styles
of doing reinforcement learning, one in which we learn to behave without trying to understand the dynamics
of the environment. And in the other hand, we learn to behave by simultaneously trying to learn the environment
so that our learning could become more and more accurate each time.

For this, we will look into a couple of algorithms for model-free reinforcement learning and we will also look
at an algorithm that tries to learn the model with each observation and become much more efficient with every
iteration.

Lesson 4 Notebook.

#### 4.7 Further Readings


## Part III: Decision-Making in Hard Problems

### 5. Discrete and Continuous States

#### 5.1 Too large to hold in memory

#### 5.2 Discretizition of state space

#### 5.3 Use of function approximation

#### 5.4 Exercises

In this lesson we got a step closer to what we could call 'real-world' reinforcement learning. In specific,
we look at a kind of environment in which there are so many states that we can no longer represent a table
of all of them. Either because the state space is too large or flat out continuous.

In order to get a sense for this type of problem we will look a basic Cart Pole pole, and we will solve it by
discretizing the state space in a way to making a manual function approximation of this problem.

Lesson 5 Notebook.

#### 5.5 Further Readings

### 6. Discrete and Continuous Actions

#### 6.1 Continous action space

#### 6.2 Discretizition of action space

#### 6.3 Use of function approximation

#### 6.4 Searching for the policy

#### 6.5 Exercises

In this lesson we looked for the first time at the a problem in which the both the number of states and the number
of actions available to the agent are very large or continuous. We introduced a series of methods based on policy
search. So, for this lesson's Notebook we will look into a problem with continuous state and actions and we
will apply function approximation to come up with the best solution to it.

Lesson 6 Notebook.

#### 6.6 Further Readings


### 7. Observable and Partially-Observable States

#### 7.1 Is what we see what it is?

#### 7.2 State Estimation

#### 7.3 Control in Partially-Observable Environments

#### 7.4 Exercises

In this lesson we learned that what we see is not always what it is happening in the world. Our perceptions might be
biased, we might not have a 20/20 vision and more importantly we might think we have 20/20 but we might not. For this
reason is important to know that there are other ways of estimating states. In the following Notebook we will look
at a very popular method for state estimation called the Kalman Filter for a very basic problem partially-observable
states problem.

#### 7.5 Further Readings

## Part IV: Multiple Decision-Making Agents

### 8. Single and Multiple Agents

#### 8.1 Agents with same objectives

#### 8.2 What when other agents are at play?

#### 8.3 Exercises

In this lesson we opened up ourselves to the world of multiple agents. This lesson concentrated on
contrasting single and multiple agents, however, there is more than just that, we know that
multiple agents can be helping our objective or getting us away from our goal. For now, the next Notebook
will try to help us understand the fundamentals of game theory necessary to take optimal decision in a world
or many. Later we will look at specific environments of multi-agent reinforcement learning.

Lesson 8 Notebook.

#### 8.4 Further Readings

### 9. Cooperative and Adversarial Agents

#### 9.1 Agents with conflicting objectives

#### 9.2 Teams of agents with conflicting objectives

#### 9.3 Exercises

In this lesson we looked into how things change when we interact with other agents, and these agents can be
cooperative, or adversarial or perhaps a combination of both if we think adversarial teams. For this lesson,
and to close up on the series of Notebooks well, we will look into the world of gym-soccer environments.

Lesson 9 Notebook.

#### 9.4 Further Readings

## Part V: Human Decision-Making and Beyond

### 10. Decision-Making and Humans

#### 10.1 Similarities between methods discussed and humans

#### 10.2 Differences between methods discussed and humans

#### 10.3 Further Readings

### 11. Conclusion

### 12. References

