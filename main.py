''' Public Goods Game Simulation '''

import pandas as pd
import numpy as np
import classes
import random

Roster = classes.Roster
PGG_Instance = classes.PGG_Instance

K = 10000  # Number of instances
NUM_OF_ROUNDS = 10  # Number of rounds per an instance
k_instances = {}
k_dfs = {}
player_types = ['TF', 'DTF'] # List of player models

for i in range(K):
    test = Roster()

    # Parameters are randomly chosen
    beta1_dist = np.random.default_rng().uniform(0, 1.25, 5)
    beta2_dist = np.random.default_rng().uniform(0, 1.25, 5)
    disc_dist = np.random.default_rng().uniform(0, 1, 5)
    type_choice = player_types[random.randint(0,1)]

    # Game players are initialized
    for (b1,b2,disc) in zip(beta1_dist,beta2_dist,disc_dist):
        test.add_player((b1,b2,disc), type=type_choice)

    inst = PGG_Instance(test, NUM_OF_ROUNDS)
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
df.to_csv(f'K_{K!r}.csv')
