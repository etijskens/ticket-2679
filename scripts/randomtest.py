#!/usr/bin/env python3

import sys
import os

sys.path.append(os.getcwd())

import numpy as np
import pickle

import multiprocessing as mp
from functools import partial

import time

# Number of simulations and parallellism:
N_tot = 1000  # Total number of calculations
poolsize = mp.cpu_count()  # Local PC
poolsize = 10
# poolsize = int(os.environ['SLURM_CPUS_PER_TASK'])   # Slurm HPC
N_tasks = poolsize  # Each task is sent to a worker (thread) for completion.
N_per_thread = int(np.ceil(N_tot / N_tasks))

print('poolsize =', poolsize)


# Single thread function:

def OneThread_minimal_calc(dummy, N_samples):
    """ Runs minimal sampling computation on a single thread. """

    thread_result = np.zeros(N_samples)

    for i_sample in range(N_samples):
        a_sample = np.random.standard_normal(1)

        thread_result[i_sample] = a_sample

    return thread_result


# Multiprocessing pool:

if __name__ == '__main__':
    OneThread_minimal_calc_process = partial(OneThread_minimal_calc, N_samples=N_per_thread)

    tic = time.time()

    # Open parallel pool:
    # pool = mp.Pool(poolsize,initializer=np.random.seed)
    pool = mp.Pool(poolsize)

    # Run samplings in parallel:
    results = pool.map(OneThread_minimal_calc_process, range(N_tasks), chunksize=1)

    # Close pool:
    pool.close()
    pool.join()

    # Print computation time:
    toc = time.time()
    elapsed_min = (toc - tic) / 60

    print('elapsed minutes =', str(elapsed_min))

# Print all single-thread runs in the results array:

if __name__ == '__main__':
    print('comparison =', list(all(results[0] == results[i]) for i in range(1, poolsize)))
    print('results =')
    print(list(results[i][0:3] for i in range(len(results))))

