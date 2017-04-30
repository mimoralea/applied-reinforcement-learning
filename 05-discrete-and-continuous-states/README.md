## Part III: Decision-Making in Hard Problems

### 5. Discrete and Continuous States

#### 5.1 Too large to hold in memory

The truth is, as we use all previous methods to solve decision-making problems, 
it will be a time when the problems are very large. Some problems become so large that we can no longer represent it in computer memory. Moreover, even if we could hold a table with all state and action pair in memory, collecting experience for every state, action combination would be inefficient. 

#### 5.2 Discretization of state space

One way of approaching this problem is to combine states into buckets by similarity. 
This approach could effectively reduce the number of states of the problem to a 
number that allows us to solve the problem using one of the methods seen in previous
lessons. For example, in the OpenAI Lunar Lander world, we can see how the entire
right side of the landing pad and the left side could be counted as 2 unique states. 
Truth is, no matter where in that right or left area, your best action will be flight either left or right respectively making sure you are in the middle. Additionally, 
the vertical axis could be easily in the 50% up as a single area and many smaller areas as we get closer to the landing pad. We will see how to apply discretization
to the cart-pole problem on this lesson's notebook.

#### 5.3 Use of function approximation

Quickly after looking into discretization, any Machine Learning Engineer would shake his/her head. Why not using function approximation instead of doing this by hand? This is exactly why function approximation exists. In fact, we could use
any function approximator like KNN or SVM, however, if the environment is non-linear,
then nonlinear function approximators should be used instead as without them we
might be able to find a solution that improves but never reaches convergence to
the optimal policy. Perhaps, the most popular non-linear function approximators
nowadays are neural networks. In fact, the use of neural networks that are more than 3 layers deep in combination with reinforcement learning algorithms is often grouped on a field called Deep Reinforcement Learning. This is perhaps one of the
most interesting and promising areas of reinforcement learning and we will look
into it on next lesson's notebook.

#### 5.4 Exercises

In this lesson, we got a step closer to what we could call 'real-world' reinforcement learning. In specific,
we look at a kind of environment in which there are so many states that we can no longer represent a table
of all of them. Either because the state space is too large or flat out continuous.

In order to get a sense for this type of problem, we will look a basic Cart Pole pole, and we will solve it by
discretizing the state space in a way to making a manual function approximation of this problem.

Lesson 5 Notebook.

#### 5.5 Further Reading

  * [An Analysis of Reinforcement Learning with Function Approximation](http://icml2008.cs.helsinki.fi/papers/652.pdf)
  * [Residual Algorithms: Reinforcement Learning with Function Approximation](http://www.leemon.com/papers/1995b.pdf)
  * [A Brief Survey of Parametric Value Function Approximation](http://www.cs.utexas.edu/~dana/MLClass/RL_VF.pdf)
  * [A Tutorial on Linear Function Approximators for Dynamic Programming and Reinforcement Learning](https://cs.brown.edu/people/stefie10/publications/geramifard13.pdf)
  * [Playing Atari with Deep Reinforcement Learning](https://www.cs.toronto.edu/~vmnih/docs/dqn.pdf)
  * [Function Approximation via Tile Coding: Automating Parameter Choice](http://www.cs.utexas.edu/~ai-lab/pubs/SARA05.pdf)
