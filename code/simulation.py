#!/usr/bin/env python
''' Public Goods Game Simulation '''

import pandas as pd
import numpy as np
import classes
import random
import sys

Roster = classes.Roster
PGG_Instance = classes.PGG_Instance

K = 1  # Number of instances
NUM_OF_ROUNDS = 10  # Number of rounds per an instance
k_instances = {}
k_dfs = {}
player_types = ['TF', 'DTF', 'STF', 'SST', 'FJ', 'FJ2'] # List of player models
# interval = 4  # Used this variable when doing grid search over beta1 and beta2
# def run_pgg_sim(EPS,ALPH=0):
for i in range(K):
    game = Roster()

    # Parameters are randomly chosen
    # beta1_dist = np.random.default_rng().uniform(interval/10, (interval+1)/10, 1)
    # beta2_dist = [.2]  # np.random.default_rng().uniform(interval, interval+.1, 1)
    # disc_dist = np.random.default_rng().uniform(interval/10, (interval+1)/10, 1)
    type_choice = player_types[5]  # player_types[random.randint(0,1)]

    # For stochastic player: Beta 1 & Beta 2 - aka PHI and EPSILON, probability
    # of contributing the same as previous round and probability of contributing
    # the mean of opponent's contributions from previous round
    # e = float(sys.argv[1]) # make this a bash input variable
    alpha = [float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), \
             float(sys.argv[4]),float(sys.argv[5])]
    # sample = np.random.uniform(0,1,5)  # 5 Samples from uniform RV
    # sample = np.random.binomial(1, 0.5, 5)  # 5 samples from a binomial RV
    # uni = 0.3  # Percent of players make ic from uniform dist
    # bin = 0.7  # probability that remaining players contribute 1 (Binomial)
    # uniform_signal = np.random.binomial(1, uni)

    # if uniform_signal is 1:
    #     initial_contributions = np.random.uniform(0,1,5)
    # else:
    #     coin_flip = np.random.binomial(1,bin)
    #     initial_contributions = [coin_flip for x in range(5)]  # All players have same ic
    # Fixed initial avg_contributions
    initial_contributions = [0,1,1,1,1]  # three-1s
    # Game players are initialized
    for num, ic in enumerate(initial_contributions):
        #  For SST player cache has 3 variables - eps, initial contribution,
        #   and alpha. Alpha is 0 to generate a simple stochastic player. To generate
        #   a player with uniform value option, set alpha to the probability of
        #   choosing uniform option for player.
        game.add_player((ic, alpha[num]), type=type_choice) #alpha[num]

    # Fixed game players are initialized (set parameters manually)
    # for j in range(5-len(beta1_dist)):
    #     test.add_player((.35,.4,.2), type=type_choice)

    inst = PGG_Instance(game, NUM_OF_ROUNDS)
    inst.initialization()

    # Iterate through rest of the ten rounds
    while(inst.active_status):
        inst.next_round()

    # Dataframe manipulation for csv output
    df = inst.create_instance_df()
    df['instance'] = [i+1 for x in range(NUM_OF_ROUNDS)]
    k_dfs[f'df_{i}'] = df
    if i is 0:
        continue
    else:
        k_dfs[f'df_0'] = pd.concat([k_dfs[f'df_0'],k_dfs[f'df_{i}']])

    # Logging for runtime progress.
    if i%100 is 0:
        print(f'{i} instances completed!')
df = k_dfs[f'df_0'].reset_index(drop=True)
# Save to csv - naming scheme: K_<num>_<setting description>_<interval?>_
#  <model-type>.csv
df.to_csv( f'../data/K_{K!r}_{type_choice}_alpha_{alpha!r}_'
          + f'init_four-1s.csv')

# data file naming scheme:
# K: number of instances
# (not used for SST) beta1 parameter
# (not used for SST) beta2 parameter
# model (aka player) type - homogenous (all players of same type)
# epsilon parameter
# alpha parameter, if used
# 'init' for initial contribution setting - can be one of following
#   - deterministic - half of players (2 or 3 of the 5) contribute 10
#   - uniform - players contribute from a uniform distribution (0,10)
#   - binomial - players contribute either 0 or 10, where chances of 10 are 0.3
#   - binomial-half - chances of 10 are 0.5
# (not used for SST) 3p denotes that a 3rd probability is incorporated in addition to beta1 and beta2
# where player contributes a value from uniform distribution (0,10)
