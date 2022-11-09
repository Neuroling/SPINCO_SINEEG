from scipy.io import loadmat
import scipy.io
from datetime import date
import datetime
import numpy as np
from os import path
import numpy.matlib
from SVM_decode import decode_within_SVM
from Euclidean_decode import decode_euclidean_dist
import warnings
import argparse
import sys
# %%
########## INPUT ARGS
# Arguments can be manually changed in the script or set when calling the function in the command line (recommended)
# Some arguments can be left as defults (see README)


pars = argparse.ArgumentParser()

pars.add_argument('-p','--path', help='Path to data' )
#pars.add_argument('-f','--file', help='Name of input data file' )
#pars.add_argument('-f','--file', help='Name of input data file' )
pars.add_argument('-par','--parallel', help='Run in parallel', type=int )
pars.add_argument('-s','--save', help='Save output', type=int )
pars.add_argument('-d','--decode_method', help='Name of decoding function name' )
pars.add_argument('-n','--nperms', help='Number of permutations', type=int )
pars.add_argument('-k','--nfolds', help='Number of cross validation folds', type=int )
pars.add_argument('-ts','--time_start', help='Start of epoch (ms)', type=int )
pars.add_argument('-te','--time_end', help='End of epoch (ms)', type=int )
pars.add_argument('-tt', '--time_time', help='', type=int)

args = pars.parse_args()

params_decoding = {}

if np.any(args != None):
   
    if args.path==None: raise Exception("Please enter a valid path to data file") 
    else: DataPath = args.path

    if args.file==None: raise Exception("Please enter a valid data file name")
    else: Datafile = args.file
    
    #--------------------------------------------------------
    # Read individual x files  and trial info file with Y, S and times [gfraga]
    # 
    from glob import glob

    ParData = loadmat(DataPath +'/info_trials_mvpa.mat')
    #ParData = loadmat('/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/Misc/analysis/mvpa_tutorial/data_examples/Infants_all.mat')
    files = glob(DataPath+'/s*.mat', recursive=True)
    xlist = []
    for inputfile in files:
            dat = loadmat(inputfile)            
            currX = dat['x'] 
            xlist.append(currX)
            print(inputfile)
    ParData['X'] = np.concatenate((xlist),axis=2)  # X is now the data arrays of all subjects concatenated along third dim (trials)
#    import zarr
#    with open('ParData.zarr', 'wb') as f:                
#        zarr.save('ParData_X.zarr', ParData['X']) 

    #--------------------------------------------------------

    if args.parallel==None: parforArg = 1
    else: parforArg = args.parallel

    if args.save==None: SaveAll = True
    else: SaveAll = bool(args.save)
 
    if args.decode_method==None: params_decoding['function'] = 'decode_within_SVM'
    else: params_decoding['function'] = args.decode_method

    if args.nperms==None: params_decoding['num_permutations'] = 200
    else: params_decoding['num_permutations'] = args.nperms

    if args.nfolds==None: params_decoding['L'] = 4
    else: params_decoding['L'] = args.nfolds

    if args.time_time==None:  params_decoding['timetime'] = False 
    else: params_decoding['timetime'] = bool(args.time_time)


    if args.time_start==None:
        st = ParData['times'][0][0]
    else:
        st = args.time_start
    if args.time_end==None: 
        en = ParData['times'][0][-1]+1
    else:
        en = args.time_end       
    params_decoding['Epoch_analysis'] = [ st, en ]
    

# If no command line args are used, defaults are assigned here
# File names and paths can be manually set here

else: 

    DataPath      =  "/home/d.uzh.ch/gfraga/smbmount/spinco_data/SINEEG/DiN/25subj" 
    #Datafile      = 'Infants_included.mat' # set data file for decoding here
    
    parforArg          = 1   # 0 = not parallel 1 = parallel
    SaveAll            = True # save output 

   