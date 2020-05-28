'''
Possible start:

    implement a simple model from Watts paper
    stochastic 2-step model with discount factor for impulsivity - 3 parameters per player
    variables: n, beta 1, beta 2, discount factor, and initial contribution

How should we handle initial contribution? How do other social experiment papers handle initial contribution?
Model output - determine what the variance of output is?
Which output format would be the best for our purposes? -- we will try CSV to use for statistical analysis via R

    21 columns: 15 for parameter input, 5 for each player contribution, and 1 column to denote round
    10 rows, where each row is a single round

Let's define an instance as 5 agents playing 10 rounds of PGG
Let's run each instance k times, and set k = 1000 - so that we have sufficient data to generate some decent statistical analysis
20 random instances: 10 completely random instances, 10 instances that are less random and more deliberate to explore parameter space somehow

    example to explore discount factor - fix beta 1 and beta 2 and randomize the discount factor
'''
# cli input?
# output ---> csv file

# player class
    # parameters - endowment, beta1, beta2, gamma, epsilon, epsilon-0
    # methods - contribute
# instance class
    # parameters
    # methods



def disc_two_fact_contribution(b1,b2,discount, cache):
    """Predict i^th player's contribution for current round.

    Keyword arguments:
    b1 -- beta1 coefficient
    b2 -- beta2 coefficient
    discount -- discount parameter
    cache -- cached variables: (prev_contribution, avg_prev_contributions, t)
    """
    prev_contribution, avg_prev_contributions, t = cache
    return b1*prev_contribution + b2*(1-discount**(round-t+1))/(1-discount)*avg_prev_contributions

round = 1
players = 5
b_1 = 0.9
b_2 = 0.5
gamma = 0.25

beta1_list = [b_1 for i in range(players)]
beta2_list = [b_2 for i in range(players)]
discount_list = [gamma for i in range(players)]


### Perhaps a better approach would be to create a player class, an instance class that handles player objects and also maintains "snapshots of the rounds"
