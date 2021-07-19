''' Script to compute average payoff after 10th round of each instance '''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def revise_col_names(df):
    new_df = df.rename(columns={
          'p1 beta1' : 'p1_b1', 'p1 beta2' : 'p1_b2', 'p1 discount' : 'p1_disc',
          'p2 beta1' : 'p2_b1', 'p2 beta2' : 'p2_b2', 'p2 discount' : 'p2_disc',
          'p3 beta1' : 'p3_b1', 'p3 beta2' : 'p3_b2', 'p3 discount' : 'p3_disc',
          'p4 beta1' : 'p4_b1', 'p4 beta2' : 'p4_b2', 'p4 discount' : 'p4_disc',
          'p5 beta1' : 'p5_b1', 'p5 beta2' : 'p5_b2', 'p5 discount' : 'p5_disc',
          'p1 contributions' : 'p1_cont', 'p1 e after round' : 'new_p1_e',
          'p2 contributions' : 'p2_cont', 'p2 e after round' : 'new_p2_e', 
          'p3 contributions' : 'p3_cont', 'p3 e after round' : 'new_p3_e',
          'p4 contributions' : 'p4_cont', 'p4 e after round' : 'new_p4_e',
          'p5 contributions' : 'p5_cont', 'p5 e after round' : 'new_p5_e',
          'Round #' : 'round_num'})
    return new_df


df = pd.read_csv('data/K_1000_low_tf.csv',header=0)
df = revise_col_names(df)

# Isolate player endowments to compute payouts and then each round's avg payout
payouts = df[['new_p1_e', 'new_p2_e','new_p3_e','new_p4_e','new_p5_e']]
payouts_mean = payouts.diff().mean(axis=1)

# Include avg payout as a new column to original data
df['avg_payout'] = payouts_mean

# Isolate the final round of each instance
tenth_round = df[df.round_num==10]
tenth_round_k_avg_payout = tenth_round[['instance', 'avg_payout']]

# Create boxplot to visualize distribution of the final round payout averages
fig1, ax1 = plt.subplots()
ax1.set_title('Average Payouts After Tenth Round')
ax1.set_yscale("log")
boxplt = tenth_round_k_avg_payout.boxplot(column='avg_payout', ax=ax1)
