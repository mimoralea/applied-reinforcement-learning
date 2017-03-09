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

#### 1.2 Rational Decisions

At the very basic level decision-making combines probability theory with utility theory. These
two together form a complete framework for decision-making under uncertainty known as Decision
Theory. 


#### 1.3 Modeling Problems

#### 1.4 Exercises

* Implement Bayes Network

## Part II: Reinforcement Learning and Decision-Making

### 2. Single and Sequential Decisions

#### 2.1 Single Decision

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
* Value Iteration
* Policy Search

#### 2.9 Exercises

* Implement Policy Iteration

### 3. Deterministic and Stochastic Actions

#### 3.xx Exercises

* Implement Value Iteration

### 4. Known and Unknown Environments

#### 4.xx Exercises

* Implement Q-Learning
* Implement SARSA
* Implement "Learning Model" (Guided Policy Search??)

## Part III: Decision-Making in Hard Problems

### 5. Discrete and Continuous States

#### 5.xx Exercises

* Implement DQN

### 6. Discrete Actions and Continuous Actions

#### 6.xx Exercises

* Implement Policy Search

### 7. Observable and Partially-Observable States

#### 7.xx Exercises

* Implement Kalman Filters
* Implement Monte-Carlo POMDP

## Part IV: Multiple Decision-Making Agents

### 8. Single and Multiple Agents

#### 8.xx Exercises

* Implement Dec-MDP Algorithm
* Implement Dec-POMDP Algorithm

### 9. Cooperative and Adversarial Agents

#### 9.xx Exercises

* Solve robo-soccer environment

## Part V: Human Decision-Making and Beyond

### 10. Decision-Making and Humans

### 11. Conclusion

### 12. References

