### 4. Known and Unknown Environments

#### 4.1 What if we don't have a model of the environment?

One of the first things that will come to your head after reviewing the last tutorial is, but what's the point if
we need to have the dynamics of the environment? What if it is such a complex environment that it is just too hard
to model? Or better yet, what if we just don't know the environment? Can we still learn the best actions to take
in order to maximize long term rewards?

And, the answer to that question is of course we can deal with unknown environments. Perhaps, this is the most exciting
aspect of reinforcement learning; agents are capable of, through interaction only, learning the best sequence of actions
to take to maximize long term reward.

#### 4.2 The need to explore

The fact that we do not have a map of the environment puts us in need to explore it. Before, we were given a map or as
it is called in reinforcement learning, a model (MDP), but now, we are just dropped in the middle of a world with no
other guidance than our own experiences. The need for exploration comes with a price. We can no longer take a perfect
sequence of actions that maximize the long term rewards from the very first time. Instead, we are now ensured to, at
least, fail a couple of times trying to understand the environment and attempting to reach better goals each time.

If you think about it, this puts us into a dilemma, as exploration has a cost associated with it, how much is it effective
to pay for it such that the long term rewards are maximized. For example, think about a young person graduating from college
at 20 and getting his/her first job. This person gains goes around in 3-4 different jobs early on, but later when we is 50 and
has accumulated experience in a specific field, it might no longer be beneficial to do a career change. It could be much
more effective to keep exploiting the experience he/she has gained. Even if there exists a possibility for higher reward on some
other field. Potentially, given the time left on his/her career, the price of learning a new set of skills might not benefit
the long term goals.

#### 4.3 What to learn?

There are two ways you could think of interacting with world. At first we could think of the value of taking actions on
given states. For example, we calculate the expectation of taking action 'a' when on state 's', then do the same for all
possible state, action combinations. However, as we saw on previous lessons, if we had a model of the environment, we could
determine the exact best value for each state. So, how about learning the model of the environment and then using some of
algorithms on previous lectures to help us guide our decision making?

It turns out that these two ways are the most fundamental classes of algorithms in reinforcement learning. Model-Free methods
are those algorithms that learn straight the action selection. These methods are incredibly useful as they are
capable of learning best actions without any knowledge of the environment. However, they are very data hungry and it
requires lots of samples to get good results. Practically speaking, we cannot just let a bipedal robot fall 1,000,000 times
just for the sake of gaining experience. On the other side of the spectrum, Model-Based methods learn and use the model
of the environment in order to improve the action selection especially early on. Model-Based methods are much more data
efficient and for this reason they are utilized more frequently on problems involving hardware such as robotics.

#### 4.4 What to do with what we learn?

We saw before that we will have to interact with the environment in order to learn. This obvious way of learning is
called "Online learning". In contrast, however, we could also collect the samples we get from our experience and
use that to further evaluate our actions. Intuitively we can think of how humans learn. When we interact with our
environment, we learn directly from our experiences with it, but also, after we have collected these experiences,
we use our memory to think about it and learn so more of what happened, what we did and how we could improve the
outcome if we are face the same problem again. This way of learning is called "Offline learning", and it is also
used in reinforcement learning.

#### 4.5 Adding small randomness to your actions

Finally, there is some other important point often seen in reinforcement learning. The fact that we learn a good
policy does not imply that such policy should be always followed. What if there is some better actions we could
have taken? How do we ensure we always keep an eye on yet a better policy? In reinforcement learning, there are
two main classes of algorithms that address ways of learning while constantly striving for finding better policies.
One ways is called off-policy, and it basically means that the actions taken by the agent are not necessarily always
those that we have determined as the best actions. We would then be updating the values of a policy as if we were
taking the actions of that policy, when in fact we selected the action from another policy. We can also see off-policy
as having two different policies, one that determines the actions that we are selecting, and the other the one that
we use to evaluate our action selection. Conversely, we also have on-policy learning in which we learn and act on
top of the same policy. That is, we evaluate and follow the actions from the same policy.

#### 4.6 Exercises

In this lesson we learned the difference between planning and reinforcement learning. We compared two styles
of doing reinforcement learning, one in which we learn to behave without trying to understand the dynamics
of the environment. And in the other hand, we learn to behave by simultaneously trying to learn the environment
so that our learning could become more and more accurate each time.

For this, we will look into a couple of algorithms for model-free reinforcement learning and we will also look
at an algorithm that tries to learn the model with each observation and become much more efficient with every
iteration.

Lesson 4 Notebook.

#### 4.7 Further Readings
