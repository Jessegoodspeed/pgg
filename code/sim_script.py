#!/usr/bin/env python

# Script to run simulation.py with multiple inputs

import subprocess, time
# import simulation


# Parameter lists used as inputs for player types
test_eps_params = [x/10 for x in range(1,6)] # 6
test_alpha_params = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1] # ,0.25,0.5]
alpha_param_groups = [(0.7, 0.6, 0.5, 0.65, 0.55)]#,0.4,0.6,0.8, 1.0)]
# (0.2,0.2,0.2,0.9,0.9),(0.2,0.4,0.6,0.8, 1.0), \
                      # (0.1,0.1,0.3,0.4,0.5), (0.5,0.4,0.3,0.1,0.1), \
                      # (0.3,0.3,0.5,0.7,0.7), (0.7,0.7,0.5,0.3,0.3), \
                      # (0.7,0.7,0.8,0.8,0.9), (0.9,0.8,0.8,0.7,0.7)]
start = time.time()
proc_list = []
# for e in test_eps_params:
for a in alpha_param_groups:
    a1, a2, a3, a4, a5 = a
    proc = subprocess.Popen(['./simulation.py', f'{a1!r}',f'{a2!r}',f'{a3!r}', \
                             f'{a4!r}',f'{a5!r}' ]) # 1 argument for FJ model - alpha
    proc_list.append(proc)
for proc in proc_list:
    proc.communicate()

end = time.time()
delta = end - start
print(f'Finished in {delta:.3} seconds.')
