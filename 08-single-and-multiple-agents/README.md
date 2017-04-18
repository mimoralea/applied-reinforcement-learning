## Part IV: Multiple Decision-Making Agents

### 8. Single and Multiple Agents

#### 8.1 Agents with same objectives

The methods for reinforcement learning that we have seen so far relate to single agents taking decisions 
on an environment. We can think, however, on a slightly different kind of problem in which multiple agents
jointly act on the same environment trying to maximize a common reward signal. Such environment could be 
robotics, networking, economics, auctions, etc. Often time, the algorithms discussed up until now would
potentially fail in such environments. The problem is that in these kinds of environments, the control of
the agents is decentralized and therefore it requires coordination and cooperation to maximize the reward
signal.

Even though decentralizing the decision-making adds considerable complexity, the need for multi-agent system
for some problems is real. Often a centralized approach is just not possible, perhaps due to physical 
constraints for example, a network routing system being decentralized, or a team of robots with shared 
objectives but independent processing capabilities. So, the methods of decentralized reinforcement learning,
often called Dec-MDPs and Dec-POMDPs, are very important as well.

#### 8.2 What when other agents are at play?

When other agents take actions on the same environment, game theory becomes important. Game theory is 
a field that researches conflict of interests. Economics, political science, psychology, biology and so on
are some of the most conventional fields using game theory concepts. On this lesson's notebook we will 
look at some game theory exercises.

#### 8.3 Exercises

In this lesson we opened up ourselves to the world of multiple agents. This lesson concentrated on
contrasting single and multiple agents, however, there is more than just that, we know that
multiple agents can be helping our objective or getting us away from our goal. For now, the next Notebook
will try to help us understand the fundamentals of game theory necessary to take optimal decision in a world
or many. Later we will look at specific environments of multi-agent reinforcement learning.

Lesson 8 Notebook.

#### 8.4 Further Reading
