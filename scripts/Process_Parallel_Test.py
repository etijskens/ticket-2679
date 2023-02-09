# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 12:09:59 2023
@author: Lennart

Process data of Run_Parallel_test
"""

import numpy as np
import pickle

#%%
############################################################################
# 1: import results
############################################################################

with open("results.obj",'rb') as read_results:
    loaded_results = pickle.load(read_results)
    

#%%
############################################################################
# 2: check size of results array
############################################################################

print(np.shape(loaded_results))

# This should be (64,16) --> 16 numbers generated by each of the 64 cores
    
#%%
############################################################################
# 3: check if different thread results are independent/different
############################################################################

print(loaded_results[0] == loaded_results[4])


# This should give [False False False ....] if the thread did independent calculations, but it gives [True True True ...]