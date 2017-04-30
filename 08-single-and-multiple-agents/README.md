## Part IV: Multiple Decision-Making Agents

### 8. Single and Multiple Agents

#### 8.1 Agents with same objectives

The methods for reinforcement learning that we have seen so far relate to single agents taking decisions on an environment. We can think, however, on a slightly different kind of problem in which multiple agents
jointly act on the same environment trying to maximize a common reward signal. Such environment could be robotics, networking, economics, auctions, etc. Often time, the algorithms discussed up until now would
potentially fail in such environments. The problem is that in these kinds of environments, the control of
the agents is decentralized and therefore it requires coordination and cooperation to maximize the reward
signal.

Even though decentralizing the decision-making adds considerable complexity, the need for a multi-agent system
for some problems is real. Often a centralized approach is just not possible, perhaps due to physical constraints, for example, a network routing system being decentralized, or a team of robots with shared objectives but independent processing capabilities. So, the methods of decentralized reinforcement learning,
often called Dec-MDPs and Dec-POMDPs, are very important as well.

#### 8.2 What when other agents are at play?

When other agents take actions on the same environment, game theory becomes important. Game theory is a field that researches conflict of interests. Economics, political science, psychology, biology and so on
are some of the most conventional fields using game theory concepts.

#### 8.3 Further Reading

  * [Game Theory: Basic Concepts](http://www.umass.edu/preferen/Game%20Theory%20Evolving/GTE%20Public/GTE%20Game%20Theory%20Basic%20Concepts.pdf)
  * [Game Theory](http://www.cdam.lse.ac.uk/Reports/Files/cdam-2001-09.pdf)
  * [An Analysis of Stochastic Game Theory for Multiagent Reinforcement Learning](http://www.cs.cmu.edu/~mmv/papers/00TR-mike.pdf)
  * [Multi-agent reinforcement learning: An overview](https://pdfs.semanticscholar.org/d96d/a4ac9f78924871c3c4d0dece0b84884fe483.pdf)
  * [Multi Agent Reinforcement Learning: Independent vs Cooperative Agents](http://web.media.mit.edu/~cynthiab/Readings/tan-MAS-reinfLearn.pdf)
