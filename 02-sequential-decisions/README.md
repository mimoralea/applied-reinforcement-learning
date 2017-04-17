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

#### 2.9 Further Reading
