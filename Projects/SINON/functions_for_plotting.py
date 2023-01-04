#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 17:16:48 2022

@author: gfraga
"""
#-------------------------------------------------------------------------------------
def multiplot_lines_scatter(data,xvar,yvar,yvar2,zvar,facet_var,multi_title):
    from matplotlib.gridspec import GridSpec
    import seaborn as sns
    import matplotlib.pyplot as plt

    facet_vals = data[facet_var].unique()# one plot per variable        
    #set up grid figure to fill with subplots
    fig = plt.figure(figsize=(12,10))
    fig.subplots_adjust(hspace=0.4,wspace=0.2)
    gs = GridSpec(nrows=3,ncols=len(facet_vals))
        
    for i in range(len(facet_vals)):
        d2plot = data.loc[(data[facet_var]==facet_vals[i]),] # data selection
        
        #LINE plot 
        fig.add_subplot(gs[0,i])
        ax = sns.lineplot(data=d2plot,x=xvar,y=yvar,hue=zvar,style=zvar,dashes=False,markers=["o"]*len(d2plot[zvar].unique())) 
       
        # title, horiz line, margins
        plt.title(facet_vals[i], size=15)
        plt.axhline(y = 0.5, color = 'r', linestyle = '--',linewidth=.5)
        plt.margins(y=.1)    
     
        # control legend position 
        if i == 0: ax.get_legend().remove()
        else:  plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
        
        #Add SCATTER of MISSING responses
        fig.add_subplot(gs[1,i])
        sns.scatterplot(data=d2plot,x=xvar,y=yvar2,hue=zvar,alpha=.5,x_jitter=4)
        
        #global title    
        fig.suptitle(multi_title,fontsize=18)
    
    return(fig)

#-------------------------------------------------------------------------------------

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

def multiplots_rainclouds(data,xvar,yvar,zvar,facet_var,facet_var2,multi_title,color_pals,ort):
    from matplotlib.gridspec import GridSpec
    import seaborn as sns
    import matplotlib.pyplot as plt        
    import ptitprince as pt 
  
    facet_vals = data[facet_var].unique() # one plot per variable
    facet_vals2 = data[facet_var2].unique()     

    fig = plt.figure(figsize=(20, 17))
    gs = GridSpec(nrows=1+len(facet_vals2),ncols=len(facet_vals))

    for i in range(len(facet_vals)):
        fig.add_subplot(gs[0,i])
        pal = sns.color_palette(color_pals[i],n_colors=5)
        d2plot = data.loc[(data[facet_var]==facet_vals[i]),]
        pt.RainCloud(data=d2plot,x=xvar,y=yvar, 
             width_viol=0.8,
             width_box=.4,
             orient='v',
             point_size=5,
             palette=pal)
        plt.title(facet_vals[i])
        #title.set_size(15)
        
    for i in range(len(facet_vals)):
        for j in range(len(facet_vals2)):  
            fig.add_subplot(gs[j+1,i])
            pal = sns.color_palette(color_pals[i],n_colors=5)
            d2plot = data.loc[(data[facet_var]==facet_vals[i]) & (data[facet_var2]==facet_vals2[j]),]
            pt.RainCloud(data=d2plot,x=xvar,y=yvar, 
                 width_viol=0.8,
                 width_box=.4,
                 orient=ort,
                 point_size=5,
                 palette=pal)
            plt.title('block' + str(facet_vals2[j]))  
            
            
    return(fig)