# -*- coding: utf-8 -*-
%reset -f #clear all ? 
"""
Created on Mon Oct 10 10:04:55 2022
@author: gfraga

"""
import os  # Commands to remember: os.getcwd(), os.listdir() 
import pandas as pd
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go
from plotly.tools import FigureFactory as FF

#conda install ptitprince

# Fix for issue with spyder not showing plotly 
import plotly.io as io
io.renderers.default='browser'

# inputs 
dirinput = 'V:/spinco_data/SINON/outputs'
fileinput = 'data_2FC_matthias.xlsx'
os.chdir(dirinput)

# DATA PREP
#----------------------------------------------------------------
# read data, select columns
dat = pd.read_excel(fileinput)
dat = dat.iloc[:,(dat.columns.get_loc('Checkpoint')  + 1): len(dat.columns)] #discard some initial cols

# find rows with response(rows following 'audio play requested')
df = dat.iloc[dat.index[(dat.Response == 'AUDIO PLAY REQUESTED') & (dat.display!= 'example')] + 1]

#  Get Additional audio info (type, SNR) from Audio file name
df.insert(2,"STIM",df[np.unique(df.list)]) # audio presented for this subject
df.insert(2,"TYPE",df['STIM'].str.split('norm').str[0].str.split('_').str[0])

df.insert(2,"SNR",df['STIM'].str.split('norm').str[1].str.replace('_','').str.replace('.wav','')) # use string split from filenames
df['SNR'].replace({'-10db': '1','-5db': '2', '0db': '3', '5db': '4','10db': '5',\
                   '4chans': '1','5chans': '2', '6chans': '3', '7chans': '4','8chans': '5' }, inplace=True)
    
 
# DESCRIPTIVE STATS 
#----------------------------------------------------------------
ds1 =     df.groupby(['block','TYPE','SNR'])['Correct'].describe().reset_index()
ds2 = df.groupby(['TYPE','SNR'])['Correct'].describe().reset_index()
ds2.insert(2,"block",'mean')
ds = pd.concat([ds1,ds2])

# add col specfying messure

 # add rt  



# PLOTs
#----------------------------------------------------------------
# PLOT accuracy
px.line(ds,x='SNR',y ='mean',facet_col='TYPE',color='block',markers=True, title='Accuracy')
#fig.update_traces(marker=dict(size=12, line=dict(width=2)), selector=dict(mode='markers'))
fig.show()
                  
 