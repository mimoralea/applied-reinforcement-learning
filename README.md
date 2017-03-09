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
under many different names. Economics, Neuroscience, Psychology, Operations Research,
Statistics, Optimal Control Theory, Reinforcement Learning are some of the prominent 
fields contributing to the understanding of decision-making. However, if we think a little
deeper most fields are concern with optimal decision-making. They might not necessarily
contribute directly to improving our understanding of how we take optimal decision, but
they too would benefit from learning this. For instance, think journalism. This activity
is not concerned with understanding how to take optimal decisions in general, but it is 
definitely interested in learning how to take optimal decisions in regards to preparing
news and writing for newspapers. Under this token, we can see how fields that study 
decision-making are a generalization of other fields.

In the following lessons we will explore decision-making in regards to Reinforcement 
Learning. As Reinforcement Learning is a descendant of Artificial Intelligence, we will 
briefly touch on Artificial Intelligence and also, being such a related field, Statistics.
We will have a lesson about decision-making when there is only one decision to make. This
is perhaps the major difference of Reinforcement Learning, which relaxes this constrain
and also studies problem in which agents can take multiple decision in a sequential manner. 
This sense of interaction with an environment sets Reinforcement Learning apart. We will
continue loosing constrains and presenting more abstract topics related to Reinforcement
Learning. We will explore deterministic and stochastic transitions, know and unknown
environments, discrete and continuous states, discrete and continuous actions, observable
and partially observable states, single and multiple agents, cooperative and adversarial
agents, and finally, we will put everything in the perspective of human intelligence.

#### 1.2 Modeling Decision-Making Problems

In order to attempt solving a problem, we must be able to represented in a form that would
allow us to work on it. For decision-making problems we can think of few aspects that are
common to all problems. First, we need to be able to receive percepts of the world. This 
input could directly represent the true state of the world, but not necessarily. For example,
if we are creating a bot that buys stock in the market, we can think of the current stock
price as part of the current state of the world. However, any person that has purchased stock
knows that the sell and buy price are estimates of the actual price that the stock will sell for.
For some transactions, this price is not totally accurate. Another example is the noise robotic 
sensors have. For example, GPS localization is accurate with a few meters precision. This amount
of noise could be the difference between an autonomous car driving safely or getting on an
accident with the car on the next lane. We can see how things that we "see" are
not necessarily things that "are". This distinction will come up later, for now, we can safely 
assume that our measurements are always accurate.

Secondly, all decision-making problems have available actions. For the stock bot we can think
of a few actions, sell, buy, hold. We could also add some special action such as limit sale, limit buy,
options, etc. A robot could have the actions to power a given actuator for a given time. As 
we clarified the potential of a percept not exactly representing the state of the world, actions might
not turn with the same outcome every time it is taken. That is, actions are not necessarily deterministic.
For the stock agent example, we can imagine the small probability that sending a buy request to the server
comes back with a server communication error. For example, the probability of actually executing the
transaction could be 99.9% but there is still a small chance that doesn't go through. This stochasticity
is represented as transition functions, in which taking an action on a given state returns a probability and
the sum of all transitions for a given state action pair is equal to one. One thing we need to
make clear, however, is that probabilities must always be the same. That is, we might not know the exact
probability, but they must be stationary.

Third, we have to introduce a signal so that we can evaluate our decision-making abilities. Many problems
in fields other than Reinforcement Learning represent these are cost, Reinforcement Learning refers to
these are rewards. On our stock agent, the reward could be the number of dollars made or lost from a single
transition. In a robotic task, the reward could be slightly more complex. For example, we could design an
agent that gets positive reward while staying up straight walking. Or maybe after a specific tasks is 
accomplished. The important part of the reward is that this will ultimate have big influence on how our agent
performs.

This model representation is known as Markov Decision Processes (MDP). MDP is a framework for sequential 
decision-making in problems such as those presented earlier. An MDP is composed of a tuple 
(S, A, R, T) in which S is the set of states, A is the set of actions, R is the reward function mapping
a state and action pair to a numeric value, T is the transition function mapping a probability of a state
to a state an action pair, it basically determines the probability of reaching a state given an intial
state and an action. 

We will be using MDPs moving forward, though it is important to mention that MDPs have lots of variants, 
Dec-MDP, POMDP, QMDP, AMDP, MC-POMDP, Dec-POMDP, ND-POMDPs, MMDPs are some of the most common ones. They all
represent some type of problem related to MDPs. We will be loosing up constrains and abstracting the 
MDP definition similar but new and perhaps more exiting types of problems as we go hope you enjoy it.

#### 1.4 Exercises

## Part II: Reinforcement Learning and Decision-Making

### 2. Single and Sequential Decisions

#### 2.1 Single Decision

* multi-armed bandits

#### 2.2 Utility Theory

#### 2.3 Value of Information

#### 2.4 Game Theory

#### 2.5 Sequential Decision-Making

As we saw in the previous lesson, Decision Theory allows us to make rational
decisions under uncertainty. However, we saw the process of gathering information
in other to take the single best decision. How would things change if we had multiple 
opportunities for making decisions. For example, if you knew that this was your
last day alive, you would probably make different decisions than any regular day. Perhaps,
you would take decisions that would otherwise bring bad consequences if you had other days,
or preferably, you could also take decisions that would maximize the value of today.
The reason for this is the nature of sequential problems. Sure it would feel so good to
yell at that coworker that keeps annoying you, but as you are a rational individual, or
at least you try, you rather not do it in hopes of a higher end goal. 

Understanding the notion of the sequential nature of life is one of the most important 
aspects of intelligence. Think about it, if you give your dog 10 pounds of beef he will
probably eat the entire thing even if that makes his stomach sick. We humans know better than
that. In fact, Stanford ran an experiment around the 1970's in which they found that children
who were able to wait longer for the preferred rewards tended to have better life outcomes,
as measured by SAT scores, educational attainment, body mass index, and other life measures.

#### 2.6 Modeling Sequential Problems

* MDP
* Rewards
* transitions
* policies

#### 2.7 Evaluating solutions

* Policy Evaluation

#### 2.8 Methods for obtaining solutions
* recursion
* memoization
* dynamic programming

* Policy Improvement
* Policy Iteration
* Value Iteration
* Policy Search

#### 2.9 Exercises

* Apply Policy Iteration

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

