'''

'''

import pandas as pd
import numpy as np
import classes
import random

Roster = classes.Roster
PGG_Instance = classes.PGG_Instance

k = 1000
numOfRounds = 10
k_instances = {}
k_dfs = {}

player_types = ['TF', 'DTF'] # List of player models
for i in range(k):
    test = Roster()

    # Parameters are randomly chosen
    beta1_dist = np.random.default_rng().uniform(0, 1.25, 5)
    beta2_dist = np.random.default_rng().uniform(0, 1.25, 5)
    disc_dist = np.random.default_rng().uniform(0, 1, 5)
    type_choice = player_types[random.randint(0,1)]

    # Game players are initialized
    for (b1,b2,disc) in zip(beta1_dist,beta2_dist,disc_dist):
        test.add_player((b1,b2,disc), type=type_choice)

    # Instance is initialized
    inst = PGG_Instance(test, numOfRounds)
    inst.initialization()
    while(inst.active_status):
        inst.next_round()
    df = inst.create_instance_df()
    df['instance'] = [i+1 for x in range(numOfRounds)]
    k_dfs[f'df_{i}'] = df
    if i is 0:
        continue
    else:
        k_dfs[f'df_0'] = pd.concat([k_dfs[f'df_0'],k_dfs[f'df_{i}']])

    if i%100 is 0:
        print(f'{i} instances completed!')
df = k_dfs[f'df_0'].reset_index(drop=True)
df.to_csv('k_1000.csv')
