#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 11:06:39 2024

@author: testuser

This is the script where I try to create 16 unique blocks for experiment 2

I have three lists (callSign, colour and number) and each has 8 items.
There are 512 possible combinations of these items (8*8*8)

I need to create all 16 unique and non-overlapping lists in which each element
occurs in exactly 4 combinations. 

                                                                                                                                        
"""
import os
from glob import glob
import pandas as pd
import numpy as np
import wave
import random
import itertools
import math
#%%
ls1 = ['A','B','C','D','E','F','G','H']
ls2 = [str(i) for i in range(1,9)]
ls3 = ['S','T','U','V','W','X','Y','Z']

listOfLs = [ls1, ls2, ls3]


n_allocations = 16 # How many unique & non-overlapping blocks we want
n_targets = len(ls1) # how many items are in each list (assuming they are equal)
n_possiblecombinations = n_targets**3 # possible combinations (n_targets to the power of 3)
n_trialsPerBlock = n_possiblecombinations // n_allocations

n_appearcancesPerBlock = n_trialsPerBlock // n_targets # how many times each item should appear in each block

#%% create some variables
allocation_list = np.arange(n_allocations//2)
# random.shuffle(allocation_list) # shuffle so they are randomly assigned to block
# designation_lists = {key: [] for key in range(n_allocations//1)}
designation_lists = {key: [] for key in range(n_allocations)}

#%%
item_allocation_list = np.arange(n_targets)
indexes = []
for i in range(n_targets):
    indexes += [i * 8 + item for item in item_allocation_list[:4]]
    item_allocation_list = np.roll(item_allocation_list, -1)


#%% create the unique lists
# list of every combination of ls2 and ls3
ls2ls3 = list(itertools.product(*[ls2,ls3]))
ls2ls3 = [''.join(i) for i in ls2ls3]


for y in allocation_list: # for every list we want...
    tmp_list = []
    
    for i, ls1_ in enumerate(ls1): # for every possible item on lst1
        
        for x in range(n_targets):
            ls1ls2ls3 = ''.join([ls1_, ls2ls3[x*n_targets+x]])
            tmp_list.append(ls1ls2ls3)   
        ls2ls3 = np.roll(ls2ls3, -n_targets)
        
    designation_lists[y] = [tmp_list[idx] for idx in indexes]
        
    # designation_lists[y] = tmp_list[::2]
    designation_lists[y+8] = [item for item in tmp_list if item not in designation_lists[y]]
    
    ls1 = np.roll(ls1, -1)


     
#%% check_unique if the lists are actually unique. Also check if they contain duplicates
check_unique = []
check_duplicates = []
check_n_appearances = []

# Loop over every list in the dict
for i in range(len(designation_lists)):
    
    # transforming a list to set will erase duplicates. 
    # So if len(set(someList)) != len(someList) then there are duplicates
    if len(set(designation_lists[i])) != len(designation_lists[i]):
        check_duplicates.append[i]
        print('list', i, 'contains duplicates')
    
    # check every list in the dict against every other list in the dict    
    for j in range(i+1, len(designation_lists)):
        
        # check if any items in any two lists overlap, if yes, count how many common elements
        if any(item in designation_lists[i] for item in designation_lists[j]):   
            ch_count = [item in designation_lists[i] for item in designation_lists[j]].count(True)
            print('lists', i,'and', j, 'overlap in', ch_count, 'items')
            check_unique.append([i,j,ch_count])

# check if every item occurs as many times as it should            
for key, desig_lst in enumerate(designation_lists.values()):
    for lst in listOfLs:
        for substr in lst:
            cnt = len([i for i in desig_lst if substr in i])
            if cnt != n_appearcancesPerBlock: 
                print('in List', key, "item", substr, "occurs", cnt, 'times') 
                check_n_appearances.append([key,substr,cnt])
                
if check_unique: 
    raise ValueError('lists are not unique')
if check_duplicates: 
    raise ValueError('at least one list contains duplicates')
if check_n_appearances: 
    raise ValueError('not all items appear %s times', n_appearcancesPerBlock)

            # print(str(key) + "_" + substr + "_" + str(cnt))
    # break

# for key, desig_lst in enumerate(designation_lists.values()):
#     for lst in [ls1, ls2, ls3]:
#         for substr in lst:
#             cnt = len([i for i in desig_lst if substr in i])
#             if cnt != n_appearcancesPerBlock: raise ValueError('not all items appear n_appearcancesPerBlock times')    
