# Applied Reinforcement Learning

I've been studying reinforcement learning and decision-making for a couple of years now.
One of the most difficult things that I've encountered is not necessarily related to 
the concepts but how these concepts have been explained. To me, learning occurs when one
is able to make a connection with the concepts being taught. For this, often an intuitive
explanation is required, and likely a hands-on approach helps build that kind of 
understanding.

My goal for this repository is to create, with the community, a resource that would help
newcomers understand reinforcement learning in an intuitive way. Consider what you see here
my initial attempt to teach some of these concepts as plain and simple as I can possibly
explain them.

If you'd like to collaborate, whether a typo, or an entire addition to the text, maybe a fix
to a notebook or a whole new notebook, please feel free to send your issue and/or pull 
request to make things better. As long as your pull request aligns with the goal of the 
repository, it is very likely we will merge. I'm not the best teacher, or reinforcement
learning researcher, but I do believe we can make reinforcement learning and decision-making 
easy for anyone to understand. Well, at least easier.

Table of Contents
=================

  * [Notebooks Installation](#notebooks-installation)
    * [Install git](#install-git)
    * [Install Docker](#install-docker)
    * [Run Notebooks](#run-notebooks)
        * [TL;DR version](#tldr-version)
        * [A little more detailed version:](#a-little-more-detailed-version)
          * [Open the Notebooks in your browser:](#open-the-notebooks-in-your-browser)
          * [Open TensorBoard at the following address:](#open-tensorboard-at-the-following-address)
    * [Docker Tips](#docker-tips)
  * [Part I: Introduction](01-introduction-to-decision-making/README.md#part-i-introduction)
      * [1. Introduction to Decision-Making](01-introduction-to-decision-making/README.md#1-introduction-to-decision-making)
        * [1.1 Decision-Making](01-introduction-to-decision-making/README.md#11-decision-making)
        * [1.2 Further Reading](01-introduction-to-decision-making/README.md#12-further-reading)
  * [Part II: Reinforcement Learning and Decision-Making](02-sequential-decisions/README.md#part-ii-reinforcement-learning-and-decision-making)
      * [2. Sequential Decisions](02-sequential-decisions/README.md#2-sequential-decisions)
        * [2.1 Modeling Decision-Making Problems](02-sequential-decisions/README.md#21-modeling-decision-making-problems)
        * [2.2 Solutions Representation](02-sequential-decisions/README.md#22-solutions-representation)
        * [2.2 Simple Sequential Problem](02-sequential-decisions/README.md#22-simple-sequential-problem)
        * [2.3 Slightly more complex problems](02-sequential-decisions/README.md#23-slightly-more-complex-problems)
        * [2.4 Evaluating solutions](02-sequential-decisions/README.md#24-evaluating-solutions)
        * [2.5 Improving on solutions](02-sequential-decisions/README.md#25-improving-on-solutions)
        * [2.6 Finding Optimal solutions](02-sequential-decisions/README.md#26-finding-optimal-solutions)
        * [2.7 Improving on Policy Iteration](02-sequential-decisions/README.md#27-improving-on-policy-iteration)
        * [2.8 Exercises](02-sequential-decisions/README.md#28-exercises)
        * [2.9 Further Reading](02-sequential-decisions/README.md#29-further-reading)
      * [3. Deterministic and Stochastic Actions](03-deterministic-and-stochastic-actions/README.md#3-deterministic-and-stochastic-actions)
        * [3.1 We can't perfectly control the world](03-deterministic-and-stochastic-actions/README.md#31-we-cant-perfectly-control-the-world)
        * [3.2 Dealing with stochasticity](03-deterministic-and-stochastic-actions/README.md#32-dealing-with-stochasticity)
        * [3.3 Exercises](03-deterministic-and-stochastic-actions/README.md#33-exercises)
        * [3.4 Further Reading](03-deterministic-and-stochastic-actions/README.md#34-further-reading)
      * [4. Known and Unknown Environments](04-known-and-unknown-environments/README.md#4-known-and-unknown-environments)
        * [4.1 What if we don't have a model of the environment?](04-known-and-unknown-environments/README.md#41-what-if-we-dont-have-a-model-of-the-environment)
        * [4.2 The need to explore](04-known-and-unknown-environments/README.md#42-the-need-to-explore)
        * [4.3 What to learn?](04-known-and-unknown-environments/README.md#43-what-to-learn)
        * [4.4 What to do with what we learn?](04-known-and-unknown-environments/README.md#44-what-to-do-with-what-we-learn)
        * [4.5 Adding small randomness to your actions](04-known-and-unknown-environments/README.md#45-adding-small-randomness-to-your-actions)
        * [4.6 Exercises](04-known-and-unknown-environments/README.md#46-exercises)
        * [4.7 Further Reading](04-known-and-unknown-environments/README.md#47-further-reading)
  * [Part III: Decision-Making in Hard Problems](05-discrete-and-continuous-states/README.md#part-iii-decision-making-in-hard-problems)
      * [5. Discrete and Continuous States](05-discrete-and-continuous-states/README.md#5-discrete-and-continuous-states)
        * [5.1 Too large to hold in memory](05-discrete-and-continuous-states/README.md#51-too-large-to-hold-in-memory)
        * [5.2 Discretization of state space](05-discrete-and-continuous-states/README.md#52-discretization-of-state-space)
        * [5.3 Use of function approximation](05-discrete-and-continuous-states/README.md#53-use-of-function-approximation)
        * [5.4 Exercises](05-discrete-and-continuous-states/README.md#54-exercises)
        * [5.5 Further Reading](05-discrete-and-continuous-states/README.md#55-further-reading)
      * [6. Discrete and Continuous Actions](06-discrete-and-continuous-actions/README.md#6-discrete-and-continuous-actions)
        * [6.1 Continuous action space](06-discrete-and-continuous-actions/README.md#61-continuous-action-space)
        * [6.2 Discretizition of action space](06-discrete-and-continuous-actions/README.md#62-discretizition-of-action-space)
        * [6.3 Use of function approximation](06-discrete-and-continuous-actions/README.md#63-use-of-function-approximation)
        * [6.4 Searching for the policy](06-discrete-and-continuous-actions/README.md#64-searching-for-the-policy)
        * [6.5 Exercises](06-discrete-and-continuous-actions/README.md#65-exercises)
        * [6.6 Further Reading](06-discrete-and-continuous-actions/README.md#66-further-reading)
      * [7. Observable and Partially-Observable States](07-observable-and-partially-observable-states/README.md#7-observable-and-partially-observable-states)
        * [7.1 Is what we see what it is?](07-observable-and-partially-observable-states/README.md#71-is-what-we-see-what-it-is)
        * [7.2 State Estimation](07-observable-and-partially-observable-states/README.md#72-state-estimation)
        * [7.3 Control in Partially-Observable Environments](07-observable-and-partially-observable-states/README.md#73-control-in-partially-observable-environments)
        * [7.4 Exercises](07-observable-and-partially-observable-states/README.md#74-exercises)
        * [7.5 Further Reading](07-observable-and-partially-observable-states/README.md#75-further-reading)
  * [Part IV: Multiple Decision-Making Agents](08-single-and-multiple-agents/README.md#part-iv-multiple-decision-making-agents)
      * [8. Single and Multiple Agents](08-single-and-multiple-agents/README.md#8-single-and-multiple-agents)
        * [8.1 Agents with same objectives](08-single-and-multiple-agents/README.md#81-agents-with-same-objectives)
        * [8.2 What when other agents are at play?](08-single-and-multiple-agents/README.md#82-what-when-other-agents-are-at-play)
        * [8.3 Exercises](08-single-and-multiple-agents/README.md#83-exercises)
        * [8.4 Further Reading](08-single-and-multiple-agents/README.md#84-further-reading)
      * [9. Cooperative and Adversarial Agents](09-cooperative-and-adversarial-agents/README.md#9-cooperative-and-adversarial-agents)
        * [9.1 Agents with conflicting objectives](09-cooperative-and-adversarial-agents/README.md#91-agents-with-conflicting-objectives)
        * [9.2 Teams of agents with conflicting objectives](09-cooperative-and-adversarial-agents/README.md#92-teams-of-agents-with-conflicting-objectives)
        * [9.3 Exercises](09-cooperative-and-adversarial-agents/README.md#93-exercises)
        * [9.4 Further Reading](09-cooperative-and-adversarial-agents/README.md#94-further-reading)
  * [Part V: Human Decision-Making and Beyond](10-decision-making-and-humans/README.md#part-v-human-decision-making-and-beyond)
      * [10. Decision-Making and Humans](10-decision-making-and-humans/README.md#10-decision-making-and-humans)
        * [10.1 Similarities between methods discussed and humans](10-decision-making-and-humans/README.md#101-similarities-between-methods-discussed-and-humans)
        * [10.2 Differences between methods discussed and humans](10-decision-making-and-humans/README.md#102-differences-between-methods-discussed-and-humans)
        * [10.3 Further Reading](10-decision-making-and-humans/README.md#103-further-reading)
      * [11. Conclusion](11-conclusion/README.md#11-conclusion)
      * [12. Recommended Books](12-recommended-books/README.md#12-recommended-books)
      * [12. Recommended Courses](13-recommended-courses/README.md#13-recommended-courses)



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

         
