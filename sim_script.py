#!/usr/bin/env python

# Script to run simulation.py with multiple inputs

import subprocess, time
# import simulation

test_eps_params = [x/10 for x in range(1,6)] # 6
test_alpha_params = [0,0.1,0.25,0.5]

start = time.time()
proc_list = []
for e in test_eps_params:
    for a in test_alpha_params:
        proc = subprocess.Popen(['./simulation.py', f'{e!r}', f'{a!r}'])
        proc_list.append(proc)
for proc in proc_list:
    proc.communicate()

end = time.time()
delta = end - start
print(f'Finished in {delta:.3} seconds.')
