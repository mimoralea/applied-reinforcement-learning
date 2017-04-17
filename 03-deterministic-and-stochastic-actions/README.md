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

#### 3.4 Further Reading

