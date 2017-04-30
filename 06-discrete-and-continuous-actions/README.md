### 6. Discrete and Continuous Actions

#### 6.1 Continous action space

Just as the state space, the action space can also become too large to handle in a
traditional way. Certainly, the problems that we have seen so far have very few
available actions, "move up, down, left, right". However, in other types of problems,
like robotics, for instance, even a small number of degrees of freedom can make the
action space just too large for traditional methods.

#### 6.2 Discretizition of action space

For the action space, discretization is commonly used. This is a fine method for
problems like we have seen before. However, once we enter the realm of physical control, which often deals with continuous values, every new degree of freedom would exponentially increase the number of possible action combinations. This gets out of control quickly.

#### 6.3 Use of function approximation

The use of function approximation is again a good way of approaching this problem. 
Just as before, linear and non-linear function approximation methods could work as 
long as we are dealing with a linear or non-linear action space, respectively.

#### 6.4 Searching for the policy

One way of approaching reinforcement learning problems that we haven't covered yet is to, instead of calculating values with states and action pairs to come up with
optimal policies, we can search for the optimal policy directly. There are different
ways of doing this and this is, in fact, one of the fields of active research in reinforcement learning. One of the advantages of using policy search instead of some
of the methods we have seen before is that it is possible we find the optimal policy
even if we don't find optimal values. For example, you can think of the trading agent
looking to calculate what's the value of buying a stock now, whether it is $10,000 or 
$100,000 you don't care the precise value, you care to know that it is the best action
to take right now. This is because you care about the policy, not the values. The
same concept applies to policy search. You could apply traditional search methods or just gradient descent to search directly for the optimal policy. We will look at
a method that searches for the optimal policy on a continuous state space and continuous
action space in the notebook.

#### 6.5 Exercises

In this lesson, we looked for the first time at the problem in which the both the number of states and the number
of actions available to the agent are very large or continuous. We introduced a series of methods based on policy
search. So, for this lesson's Notebook, we will look into a problem with continuous state and actions and we
will apply function approximation to come up with the best solution to it.

Lesson 6 Notebook.

#### 6.6 Further Reading

  * [Reinforcement Learning in Continuous State and Action Spaces](http://oai.cwi.nl/oai/asset/19689/19689B.pdf)
  * [Continuous Control with Deep Reinforcement Learning](https://arxiv.org/pdf/1509.02971.pdf)
  * [Reinforcement Learning in Continuous Action Spaces through Sequential Monte Carlo Methods](https://papers.nips.cc/paper/3318-reinforcement-learning-in-continuous-action-spaces-through-sequential-monte-carlo-methods.pdf)
  * [Q-Learning in Continuous State and Action Spaces](http://users.cecs.anu.edu.au/~rsl/rsl_papers/99ai.kambara.pdf)
  * [Deep Reinforcement Learning: An Overview](https://arxiv.org/pdf/1701.07274.pdf)
