#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 8 10:59:49 2023

Run Minimal parallel simulation

@author: lennart
"""

#%%

import sys
import os
sys.path.append(os.getcwd())

import numpy as np
import pickle

import multiprocessing as mp
from functools import partial

import time



############################################################################
# 1: Units and parameters:
############################################################################


# -----------
# Number of simulations and parallellism:
# -----------
N_tot = 1000                                        # Total number of calculations
### ET: make sure that poolsize is set independently of where we are running
try:
    poolsize = int(os.environ['SLURM_CPUS_PER_TASK'])   # Slurm HPC, i.e. compute node
except KeyError:
    poolsize = mp.cpu_count()                           # Local PC or login node

N_tasks = poolsize                                  # Each task is sent to a worker (thread) for completion.
N_per_thread = int(np.ceil(N_tot / N_tasks))


# -----------
# Print some CPU data:
# -----------
f = open( 'poolsize_file.txt', 'w' )
f.write( 'poolsize = ' +  str(poolsize) )
f.close()



#%%        
################################################################################
# 2: Single thread function:
################################################################################

def OneThread_minimal_calc(dummy, N_samples):
    """ Runs minimal sampling computation on a single thread. """

    print("ET: OneThread_minimal_calc() running on", mp.current_process()) # ET
    state = np.random.get_state()
    thread_result = np.zeros(N_samples)
    
    for i_sample in range(N_samples):
        
        a_sample = np.random.standard_normal(1)
        
        thread_result[i_sample] = a_sample

    print(f"ET: {mp.current_process()}\n{thread_result}") # ET
    return thread_result, state



#%%        
################################################################################
# 3: Multiprocessing pool:
################################################################################

OneThread_minimal_calc_process = partial(OneThread_minimal_calc, N_samples=N_per_thread)
        
if __name__ == '__main__': 
    
    tic = time.time()
    
    # -----------
    # Open parallel pool:
    # -----------         
    pool = mp.Pool(poolsize)
    print(f"ET: {pool=}")

    # ----------- 
    # Run samplings in parallel:
    # ----------- 
    print("ET: __main__ running on", mp.current_process())  # ET
    print("ET: N_tasks =", N_tasks)
    results = pool.map(OneThread_minimal_calc_process, range(N_tasks), chunksize=1)

    # -----------  
    # Close pool:
    # -----------  
    pool.close()
    pool.join()
    
    # -----------
    # Print computation time:
    # -----------
    toc = time.time()
    elapsed_min = (toc - tic)/60
    
    f = open( 'elapsed_minutes.txt', 'w' )
    f.write( 'elapsed minutes = ' +  str(elapsed_min) )
    f.close()

    

#%%
############################################################################
# 4: Save all single-thread runs in the results array:
############################################################################

if __name__ == '__main__': 
        
    with open("results.obj",'wb') as write_results:
        pickle.dump(results, write_results)
        
        
    


