# Applied Reinforcement Learning

This repository will contain a series of lessons about Reinforcement Learning and Decision Making.

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
a policy. This is important to understand and remember.

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
have already acquire. This fundamental trade-off between exploration versus exploitation is what makes 
decision-making problems hard. You might believe that a particular arm has a fairly high payoff probability; 
should you then choose it every time? Should you choose one that you know well in order to gain information
about it's payoff? How about choosing one that you might have good information already but perhaps getting more
would improve your knowledge of the environment? 

All of the answers to the questions posed above depend on several factors. For example, if instead of allowing you
100 trials I give you 3, how would your strategy change. Moreover, if I give you an infinite number of trials,
then you really want to put time learning the environment even if doing so gives you sub-optimal results. The
knowledge that you gain from the initial exploration will ensure you maximize the expected future rewards.

#### 2.3 Evaluating solutions

code:
* Policy Evaluation

#### 2.8 Methods for obtaining solutions

* recursion
* memoization
* dynamic programming

code:
* Policy Improvement
* Policy Iteration
mention:
* Value Iteration
* Policy Search

#### 2.9 Exercises

* Apply Policy Iteration to a problem

### 3. Deterministic and Stochastic Actions

#### 3.xx Exercises

* Apply Value Iteration

### 4. Known and Unknown Environments

* model-based methods
* model-free methods
* online and offline
* on-policy and off-policy
* Learning the model

#### 4.xx Exercises

* Apply TD(Lambda)
* Apply Q-Learning
* Apply SARSA
* Apply "Learning Model" (Guided Policy Search??)

## Part III: Decision-Making in Hard Problems

### 5. Discrete and Continuous States

#### 5.xx Exercises

* Apply DQN

### 6. Discrete Actions and Continuous Actions

#### 6.xx Exercises

* Apply Policy Search

### 7. Observable and Partially-Observable States

#### 7.xx Exercises

* Apply Kalman Filters
* Apply Monte-Carlo POMDP

## Part IV: Multiple Decision-Making Agents

### 8. Single and Multiple Agents

#### 8.xx Exercises

* Apply Dec-MDP Algorithm
* Apply Dec-POMDP Algorithm

### 9. Cooperative and Adversarial Agents

#### 9.xx Exercises

* Apply to robo-soccer environment

## Part V: Human Decision-Making and Beyond

### 10. Decision-Making and Humans

### 11. Conclusion

### 12. References

