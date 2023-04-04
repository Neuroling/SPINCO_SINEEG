#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 17:16:48 2022

@author: gfraga
"""
def multiplot_lines(data,xvar,yvar,zvar,facet_var,multi_title):
    from matplotlib.gridspec import GridSpec
    import seaborn as sns
    import matplotlib.pyplot as plt        

    facet_vals = data[facet_var].unique() # one plot per variable    
    #set up grid figure to fill with subplots
    fig = plt.figure(figsize=(12,10))
    fig.subplots_adjust(hspace=0.4,wspace=0.2)
    gs = GridSpec(nrows=3,ncols= len(facet_vals))     

    for i in range(len(facet_vals)):
        d2plot = data.loc[(data[facet_var]==facet_vals[i]),] # data selection
        
        #LINE plot 
        fig.add_subplot(gs[0,i])
        ax = sns.lineplot(data=d2plot,x=xvar,y=yvar,hue=zvar,style=zvar,dashes=False,markers=["o"]*len(d2plot[zvar].unique())) 
       
        # title, horiz line, margins
        plt.title(facet_vals[i], size=15)
        plt.margins(y=.1)    
     
        # control legend position
        if i == 0: ax.get_legend().remove()
        else:  plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        
        #global title    
        fig.suptitle(multi_title,fontsize=18)
    
    return(fig)

#-------------------------------------------------------------------------------------
