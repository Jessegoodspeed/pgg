''' Public Goods Game Simulation '''

import pandas as pd
import numpy as np
import classes
import random

Roster = classes.Roster
PGG_Instance = classes.PGG_Instance

K = 1000  # Number of instances
NUM_OF_ROUNDS = 10  # Number of rounds per an instance
k_instances = {}
k_dfs = {}
player_types = ['TF', 'DTF', 'STF'] # List of player models
# interval = 4  # Used this variable when doing grid search over beta1 and beta2

for i in range(K):
    game = Roster()

    # Parameters are randomly chosen
    # beta1_dist = np.random.default_rng().uniform(interval/10, (interval+1)/10, 1)
    # beta2_dist = [.2]  # np.random.default_rng().uniform(interval, interval+.1, 1)
    # disc_dist = np.random.default_rng().uniform(interval/10, (interval+1)/10, 1)
    type_choice = player_types[2]  # player_types[random.randint(0,1)]

    # For stochastic player: Beta 1 & Beta 2 - aka PHI and EPSILON, probability
    # of contributing the same as previous round and probability of contributing
    # the mean of opponent's contributions from previous round
    b1 = 0.45
    b2 = 0.45
    # sample = np.random.uniform(0,1,5)  # 5 Samples from uniform RV
    sample = np.random.binomial(1, 0.5, 5)  # 5 samples from a binomial RV
    initial_contributions = [10 * x for x in sample]  # List of initial contributions
    # Game players are initialized
    for ic in initial_contributions:
        game.add_player((b1,b2,ic), type=type_choice)

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
df.to_csv(f'data/K_{K!r}_{b1!r}_{b2!r}_stoch_init_binomial-half_3p.csv')
