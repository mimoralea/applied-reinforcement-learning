## CS8803O03 Reinforcement Learning
### Steps to run Project 3 code

The code is contained in a single python file named `soccer.py`. To run the project, follow the steps below:

1. Clone the repository

    ```
    $ git clone https://...
    ```

2. Dependencies assumed to be installed on target machine
  1. CVXOPT with the GNU GLPK solver
  2. `numpy`
  3. `pandas`  

3. In `soccer.py` uncomment the line corresponding to the algorithm 
you want to run and then 

    ```
    $ python soccer.py
    ```

4. A data file with a timestamp will be created in the current directory. Rename the data file as `qlearning.txt`, `friend.txt`, `foe.txt` or `ceq.txt` according to the algorithm run. Then run `plotting.py` to reproduce the graphs. 

Thats it!