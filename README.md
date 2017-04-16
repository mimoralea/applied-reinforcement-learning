# Applied Reinforcement Learning

This repository will contain a series of lessons about Reinforcement Learning and Decision Making.


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
  * [Part II: Reinforcement Learning and Decision-Making](#part-ii-reinforcement-learning-and-decision-making)
      * [2. Sequential Decisions](#2-sequential-decisions)
        * [2.1 Modeling Decision-Making Problems](#21-modeling-decision-making-problems)
        * [2.2 Solutions Representation](#22-solutions-representation)
        * [2.2 Simple Sequential Problem](#22-simple-sequential-problem)
        * [2.3 Slightly more complex problems](#23-slightly-more-complex-problems)
        * [2.4 Evaluating solutions](#24-evaluating-solutions)
        * [2.5 Improving on solutions](#25-improving-on-solutions)
        * [2.6 Finding Optimal solutions](#26-finding-optimal-solutions)
        * [2.7 Improving on Policy Iteration](#27-improving-on-policy-iteration)
        * [2.8 Exercises](#28-exercises)
        * [2.9 Further Readings](#29-further-readings)
      * [3. Deterministic and Stochastic Actions](#3-deterministic-and-stochastic-actions)
        * [3.1 We can't perfectly control the world](#31-we-cant-perfectly-control-the-world)
        * [3.2 Dealing with stochasticity](#32-dealing-with-stochasticity)
        * [3.3 Exercises](#33-exercises)
        * [3.4 Further Readings](#34-further-readings)
      * [4. Known and Unknown Environments](#4-known-and-unknown-environments)
        * [4.1 What if we don't have a model of the environment?](#41-what-if-we-dont-have-a-model-of-the-environment)
        * [4.2 The need to explore](#42-the-need-to-explore)
        * [4.3 What to learn?](#43-what-to-learn)
        * [4.4 What to do with what we learn?](#44-what-to-do-with-what-we-learn)
        * [4.5 Adding small randomness to your actions](#45-adding-small-randomness-to-your-actions)
        * [4.6 Exercises](#46-exercises)
        * [4.7 Further Readings](#47-further-readings)
  * [Part III: Decision-Making in Hard Problems](#part-iii-decision-making-in-hard-problems)
      * [5. Discrete and Continuous States](#5-discrete-and-continuous-states)
        * [5.1 Too large to hold in memory](#51-too-large-to-hold-in-memory)
        * [5.2 Discretizition of state space](#52-discretizition-of-state-space)
        * [5.3 Use of function approximation](#53-use-of-function-approximation)
        * [5.4 Exercises](#54-exercises)
        * [5.5 Further Readings](#55-further-readings)
      * [6. Discrete and Continuous Actions](#6-discrete-and-continuous-actions)
        * [6.1 Continous action space](#61-continous-action-space)
        * [6.2 Discretizition of action space](#62-discretizition-of-action-space)
        * [6.3 Use of function approximation](#63-use-of-function-approximation)
        * [6.4 Searching for the policy](#64-searching-for-the-policy)
        * [6.5 Exercises](#65-exercises)
        * [6.6 Further Readings](#66-further-readings)
      * [7. Observable and Partially-Observable States](#7-observable-and-partially-observable-states)
        * [7.1 Is what we see what it is?](#71-is-what-we-see-what-it-is)
        * [7.2 State Estimation](#72-state-estimation)
        * [7.3 Control in Partially-Observable Environments](#73-control-in-partially-observable-environments)
        * [7.4 Exercises](#74-exercises)
        * [7.5 Further Readings](#75-further-readings)
  * [Part IV: Multiple Decision-Making Agents](#part-iv-multiple-decision-making-agents)
      * [8. Single and Multiple Agents](#8-single-and-multiple-agents)
        * [8.1 Agents with same objectives](#81-agents-with-same-objectives)
        * [8.2 What when other agents are at play?](#82-what-when-other-agents-are-at-play)
        * [8.3 Exercises](#83-exercises)
        * [8.4 Further Readings](#84-further-readings)
      * [9. Cooperative and Adversarial Agents](#9-cooperative-and-adversarial-agents)
        * [9.1 Agents with conflicting objectives](#91-agents-with-conflicting-objectives)
        * [9.2 Teams of agents with conflicting objectives](#92-teams-of-agents-with-conflicting-objectives)
        * [9.3 Exercises](#93-exercises)
        * [9.4 Further Readings](#94-further-readings)
  * [Part V: Human Decision-Making and Beyond](#part-v-human-decision-making-and-beyond)
      * [10. Decision-Making and Humans](#10-decision-making-and-humans)
        * [10.1 Similarities between methods discussed and humans](#101-similarities-between-methods-discussed-and-humans)
        * [10.2 Differences between methods discussed and humans](#102-differences-between-methods-discussed-and-humans)
        * [10.3 Further Readings](#103-further-readings)
      * [11. Conclusion](#11-conclusion)
      * [12. References](#12-references)



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

         
