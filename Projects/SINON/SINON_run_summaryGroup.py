# -*- coding: utf-8 -*-
#%reset -f #clear all ? 
"""
Created on Mon Oct 10 10:04:55 2022
@author: gfraga

"""
import os  # Commands to remember: os.getcwd(), os.listdir() 
import pandas as pd
import glob
import sys as sys
import seaborn as sns
import plotly.io as io
import matplotlib.pyplot as plt        

# %% 
# Fix for issue with spyder not showing plotly 
io.renderers.default='browser'
# %% 
# paths
if sys.platform=='linux':  basedir  = '/home/d.uzh.ch/gfraga/smbmount/'
else:  basedir ='V:/'

# Add custom functions 
sys.path.append(basedir + 'gfraga/scripts_neulin/Projects/SINON/')
from functions import multiplot_lines,multiplot_lines_scatter,multiplot_rainclouds,gorilla_out_preproc,gorilla_out_summary

dirinput =  basedir + 'spinco_data/SINON/outputs/data_exp_116083-v1/gathered'




# %% 
tasknames = ['PM','LD','2FC']
measure = ['ACCU']


for task in tasknames:
    for meas in measure:
        validfiles = [files for files in glob.glob(dirinput + '/**/*'+task+'-'+meas+'.csv' ,recursive=True)]
 
        #Read files of this taks and concatenate
        dfs = [pd.read_csv(fileinput) for fileinput in validfiles]
        concat_df = pd.concat(dfs, axis=0)
    
# %%
plt.close('all')
df = concat_df[(concat_df['block']!='all')]
g = sns.FacetGrid(df, col="TYPE",  row="SubjectID")
g.map_dataframe(sns.lineplot, x ='LV',y='prop_hits',hue='block',style='block')
g.map_dataframe(sns.lineplot, x ='LV',y=0.5, color='gray',linestyle='dotted')
g.map_dataframe(sns.scatterplot, x='LV', y='prop_hits', marker='o', hue='block')









# %% 
def plot_subject_value(df):
    # Create a figure and axes for each unique type value
    for type_value in df['TYPE'].unique():
        fig, axs = plt.subplots(1, len(df['LV'].unique()), figsize=(20, 5))
        fig.suptitle(type_value)

        # Create a panel for each unique level value
        for i, level_value in enumerate(df['LV'].unique()):
            ax = axs[i]
            ax.set_title(level_value)

            # Filter the dataframe for the current type and level
            level_df = df[(df['TYPE'] == type_value) & (df['LV'] == level_value)]

            # Plot the subjects on the x axis and the values on the y axis
            
            block_df = level_df[(level_df['block'] == 'all')]
            ax.bar(block_df['SubjectID'], block_df['prop_hits'])

            # Show the plot
            plt.show()


plot_subject_value(concat_df)
# %%  Summary per subject
for fileinput in validfiles: 
    #fileinput = validfiles[0]
    
    os.chdir(os.path.dirname(fileinput))
    print('[-_-] >>>> Start ' +  fileinput )
    # %  DATA PREP
    #----------------------------------------------------------------
    # read data, select columns
    dat = pd.read_csv(fileinput)         
    
    # Preprocessing 
    df = gorilla_out_preproc(dat)        
    
    #descriptive statistics
    (accu,rt) = gorilla_out_summary(df)
    
    # SAVE 
    #------
    # Tables 
    df.to_csv(df.task.unique()[0] + '-PREPROC.csv', index = False)
    accu.to_csv(df.task.unique()[0] + '-ACCU.csv', index = False)
    rt.to_csv(df.task.unique()[0] + '-RT.csv', index = False)    
    
    print('---<< done preprocessing ' +  fileinput +'. \n' )
    #del dat, df, accu, rt

    # % PLOTs
    #----------------------------------------------------------------
    # Accuracy plots 
    xvar = 'LV' ; yvar = 'prop_hits'; yvar2='count_miss' ; zvar= 'block' ; facet_var = 'TYPE' # here column that defines different plots /facets
    data = accu
    multi_title = df.task.unique()[0] + ' Accuracy (n ' + str(len(accu.SubjectID.unique())) +')'
    fi1= multiplot_lines_scatter(data,xvar,yvar,yvar2, zvar,facet_var,multi_title)
    
    # %
    # RT plots
    xvar = 'LV'; yvar = 'mean'; zvar= 'block'; facet_var = 'TYPE' # here column that defines different plots /facets
    data = rt
    multi_title= df.task.unique()[0] + ' RT (n ' + str(len(rt.SubjectID.unique()))+')'
    fi2 = multiplot_lines(data, xvar, yvar, zvar, facet_var,multi_title)
    
    # Save figures    
    outputsuffix = df.task.unique()[0] + '.jpg' 
    fi1.savefig('FIG_lin_accu_' + outputsuffix)
    fi2.savefig('FIG_lin_rt_' + outputsuffix)
    
    plt.close('all')
# %% 
# # % Rain cloud
# xvar = 'LV'; yvar = 'Reaction Time'; zvar= 'block'; 
# facet_var = 'TYPE' ; facet_var2 = 'block' 
# data = df.loc[(df['Correct']==1.0),]
# multi_title='RTs '
# ort="v";
# color_pals=['mako','rocket']
# fi3 = multiplot_rainclouds(data,xvar,yvar,zvar,facet_var,facet_var2,multi_title,color_pals,ort)
   

   
# # %% RTs per block and per correct/incorrect responses
# # blocks2plot = df.block.unique()
# fi4= sns.catplot(data=df, x="LV", y="Reaction Time", hue="Correct", 
#     kind="violin",split=True,title='RTs per Block and correctness',col='TYPE',row='block',
#     inner='stick',palette='pastel')


#     #%% 
   
    #fi3.savefig('FIG_rain_rt_' + fileinput.replace('.csv','.jpg'))
    #fi4.savefig('FIG_vio_rt_' + fileinput.replace('.csv','.jpg'))
    
    
    










