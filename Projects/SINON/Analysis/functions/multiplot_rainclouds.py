#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 17:16:48 2022

@author: gfraga
"""
def multiplot_rainclouds(data,xvar,yvar,zvar,facet_var,facet_var2,multi_title,color_pals,ort):
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
