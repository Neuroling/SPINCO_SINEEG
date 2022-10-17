# -*- coding: utf-8 -*-
#%reset -f #clear all ? 
"""
Created on Mon Oct 10 10:04:55 2022
@author: gfraga

"""
import os  # Commands to remember: os.getcwd(), os.listdir() 
import pandas as pd
import numpy as np 
import sys as sys
import plotly.express as px
import plotly.graph_objects as go
from plotly.tools import FigureFactory as FF
import plotly.io as io
import seaborn as sns
import matplotlib.pyplot as plt
import ptitprince as pt
# %% 
# Fix for issue with spyder not showing plotly 
io.renderers.default='browser'

# paths
if sys.platform=='linux':  basedir  = '/home/d.uzh.ch/gfraga/smbmount/'
else:  basedir ='V:/'

scriptsdir = basedir + 'gfraga/scripts_neulin/Projects/SINON_experiment/'
sys.path.insert(0,scriptsdir)

dirinput =  basedir + 'spinco_data/SINON/outputs'
diroutput = basedir + '/spinco_data/SINON/outputs'
fileinput = 'data_2FC_matthias.xlsx'
os.chdir(dirinput)

# %%  DATA PREP
#----------------------------------------------------------------
from functions_for_preprocessing import *
# read data, select columns
dat = pd.read_excel(fileinput)
df = preprocess_gorilla_output(dat)
(accu,rt) = describe_gorilla_output(df)
            
df.to_csv(r'prep_'+fileinput.replace('.xlsx','.csv'), index = False)
# %% PLOTs
#----------------------------------------------------------------
#load plotting functions
from functions_for_plotting import *
# Accuracy plots 
xvar = 'LV' ; yvar = 'prop_hits'; yvar2='count_miss' ; zvar= 'block' ; facet_var = 'TYPE' # here column that defines different plots /facets
data = accu
multi_title = 'Summary accuracy'
fi1= multiplot_lines_scatter(data,xvar,yvar,yvar2, zvar,facet_var,multi_title)

# %
# RT plots
xvar = 'LV'; yvar = 'mean'; zvar= 'block'; facet_var = 'TYPE' # here column that defines different plots /facets
data = rt
multi_title= 'RT summary'
fi2 = multiplot_lines(data, xvar, yvar, zvar, facet_var,multi_title)

# % Rain cloud
xvar = 'LV'; yvar = 'Reaction Time'; zvar= 'block'; 
facet_var = 'TYPE' ; facet_var2 = 'block' 
data = df.loc[(df['Correct']==1.0),]
multi_title='RTs '
ort="v";
color_pals=['mako','rocket']
fi3 = multiplots_rainclouds(data,xvar,yvar,zvar,facet_var,facet_var2,multi_title,color_pals,ort)
      
# %% RTs per block and per correct/incorrect responses

# blocks2plot = df.block.unique()
fi4= sns.catplot(data=df, x="LV", y="Reaction Time", hue="Correct", 
    kind="violin",split=True,title='RTs per Block and correctness',col='TYPE',row='block',
    inner='stick',palette='pastel')

# %%  SAVE 
os.chdir(diroutput)
fi1.savefig('FIG_lin_accu.jpg')
fi2.savefig('FIG_lin_rt.jpg')
fi3.savefig('FIG_rain_rt.jpg')
fi4.savefig('FIG_vio_rt.jpg')















