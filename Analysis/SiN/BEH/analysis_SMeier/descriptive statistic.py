# -*- coding: utf-8 -*-
"""
Created on Fri Feb 16 05:33:04 2024

@author: sibme
"""

# Library installations: 
#conda install -c plotly plotly 
#conda install -c conda-forge itables
# ------------------------------------------------------------------
import sys
import os
import glob
import re
import pandas as pd
import numpy as np
import plotly.express as px 
from itables import init_notebook_mode, show 
from datetime import date
today = date.today()
#print("Run date:", today)

#%% File paths
thisScriptDir = os.getcwd()
baseDir = thisScriptDir[:thisScriptDir.find("Scripts")]
dirinput = os.path.join(baseDir + 'a','Data','SiN','analysis','beh','task-sin')
diroutput = os.path.join(baseDir + 'a','Data','SiN','analysis','beh','task-sin')

# Find file read data set 
fileinput =  [os.path.join(dirinput, f) for f in os.listdir(dirinput) if f.startswith('Gathered_')]
df = pd.read_csv(fileinput[0], index_col=None)

# Relabel noise levels
levelmapping = {'0.6p': '1_easy','0.4p': '2_mid','0.2p': '3_hard','-7db': '1_easy','-9db': '2_mid','-11db': '3_hard'}
df['levels'] = df['levels'].replace(levelmapping) 

print(' Table read with ' + str(len(df)) + ' rows and ' + str(len(df. columns)) + ' columns')
#show(df, scrollY="400px", scrollCollapse=True, paging=False)

#%% Transform to long

df_long= pd.melt(df, id_vars=['subj','noise','block','voice','levels','sentence','callSign','colour','number'],value_vars=['callSignCorrect', 'colourCorrect','numberCorrect'],
                 value_name='accu', var_name='position')

 
df_long['accu'] = df_long['accu'].astype(int)
show(df_long)
#%% Summarize accuracy score

# Define how many unique targets
unique_levels = {col: df_long[col].nunique() for col in ['block','levels','noise','position','voice']} 
print(unique_levels)
unique_targets = sum(unique_levels.values()) + 4 # there are 4 possible items  at each position in this experiment   

# Summarize Accuracies 
df_long_accu = df_long.groupby(['subj','noise', 'block', 'voice', 'levels','position'])['accu'].sum().reset_index()
df_long_accu['accu']/=unique_targets
 

show(df_long_accu)

#%% Deskriptiv Statistik

# Statistische Masse: mean, std, min, 25%, 50%, 75%, max für noise 'NV' und 'SiSSN'

# Gruppieren nach 'noise' und Berechnen der statistischen Masse für 'accu'
stats_noise = df_long_accu.groupby('noise')['accu'].describe()

# Ergebnisse anzeigen
print("Statistische Masse für NV und SiSSN:")
print(stats_noise)

#Statistische Masse: mean, std, min, 25%, 50%, 75%, max für noise 'NV'/'SiSSN' und 'levels' 

# Gruppieren des DataFrames nach "noise" und "levels"
stats_noise_levels = df_long_accu.groupby(['noise', 'levels'])['accu'].describe()

# Ergebnisse anzeigen
print("Statistische Masse für NV und SiSSN:")
print(stats_noise_levels)

# Statistische Masse: mean, std, min, 25%, 50%, 75%, max für noise 'NV'/'SiSSN' und 'block' 

# Gruppieren nach 'noise' und 'block' und Berechnen der statistischen Masse für 'accu'
stats_noise_block = df_long_accu.groupby(['noise', 'block'])['accu'].describe()

# Filtern nach 'NV' und 'SiSSN'
stats_NV_block = stats_noise_block.loc['NV']
stats_SiSSN_block = stats_noise_block.loc['SiSSN']

# Ergebnisse anzeigen
print("Statistische Masse für NV:")
print(stats_NV_block)

print("\nStatistische Masse für SiSSN:")
print(stats_SiSSN_block)

# Statistische Masse: mean, std, min, 25%, 50%, 75%, max für noise 'NV'/'SiSSN' und 'position' 

# Gruppieren nach 'noise' und 'position' und Berechnen der statistischen Masse für 'accu'
stats_noise_position = df_long_accu.groupby(['noise', 'position'])['accu'].describe()

# Filtern nach 'NV' und 'SiSSN'
stats_NV_position = stats_noise_position.loc['NV']
stats_SiSSN_position = stats_noise_position.loc['SiSSN']

# Ergebnisse anzeigen
print("Statistische Masse für NV nach Position:")
print(stats_NV_position)

print("\nStatistische Masse für SiSSN nach Position:")
print(stats_SiSSN_position)

#%% Raincloud-Plots

import matplotlib.pyplot as plt
import ptitprince as pt

# Raincloud-Plot für noise 'NV' und 'SiSSN'
plt.figure(figsize=(10, 6))
ax = pt.RainCloud(x='noise', y='accu', data=df_long_accu, width_viol=0.6, width_box=0.1)
plt.xlabel('Rauschen')
plt.ylabel('Genauigkeit')
plt.title('Raincloud Plot für Genauigkeit bei NV und SiSSN')
plt.show()

#%% Raincloud-Plot für noise 'NV'/'SiSSN' und 'levels' 

# Filtern des DataFrames für 'NV' und 'SiSSN'
df_NV = df_long_accu[df_long_accu['noise'] == 'NV']
df_SiSSN = df_long_accu[df_long_accu['noise'] == 'SiSSN']

# Raincloud-Plot für 'NV' erstellen
plt.figure(figsize=(10, 6))
ax1 = pt.RainCloud(x='levels', y='accu', data=df_NV, jitter=0.2, alpha=0.7, width_viol=0.5, width_box=0.1)
plt.xlabel('Levels')
plt.ylabel('Genauigkeit')
plt.title('Raincloud Plot für Genauigkeit der Levels (NV)')
plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Festlegen der y-Achsenticks
plt.show()

# Raincloud-Plot für 'SiSSN' erstellen
plt.figure(figsize=(10, 6))
ax2 = pt.RainCloud(x='levels', y='accu', data=df_SiSSN, jitter=0.2, alpha=0.7, width_viol=0.5, width_box=0.1)
plt.xlabel('Levels')
plt.ylabel('Genauigkeit')
plt.title('Raincloud Plot für Genauigkeit bei Levels (SiSSN)')
plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Festlegen der y-Achsenticks
plt.show()

# Raincloud-Plot für 'NV' und 'SiSSN' nebeneinander abbilden
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Raincloud-Plot für 'NV' erstellen
ax1 = pt.RainCloud(x='levels', y='accu', data=df_NV, jitter=0.2, alpha=0.7, width_viol=0.5, width_box=0.1, ax=axes[0])
ax1.set_xlabel('Levels')
ax1.set_ylabel('Genauigkeit')
ax1.set_title('Raincloud Plot für Genauigkeit der Levels (NV)')
ax1.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Festlegen der y-Achsenticks

# Raincloud-Plot für 'SiSSN' erstellen
ax2 = pt.RainCloud(x='levels', y='accu', data=df_SiSSN, jitter=0.2, alpha=0.7, width_viol=0.5, width_box=0.1, ax=axes[1])
ax2.set_xlabel('Levels')
ax2.set_ylabel('Genauigkeit')
ax2.set_title('Raincloud Plot für Genauigkeit bei Levels (SiSSN)')
ax2.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Festlegen der y-Achsenticks

plt.tight_layout()  # Platz zwischen den Subplots einstellen
plt.show()


#%% Raincloud-Plot für noise 'NV'/'SiSSN' und 'block' 

# Raincloud-Plot für 'NV' erstellen
plt.figure(figsize=(10, 6))
ax1 = pt.RainCloud(x='block', y='accu', data=df_NV, jitter=0.2, alpha=0.7, width_viol=0.5, width_box=0.1)
plt.xlabel('Block')
plt.ylabel('Genauigkeit')
plt.title('Raincloud Plot für Genauigkeit bei Block 1 & 2 (NV)')
plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Festlegen der y-Achsenticks
plt.show()

# Raincloud-Plot für 'SiSSN' erstellen
plt.figure(figsize=(10, 6))
ax2 = pt.RainCloud(x='block', y='accu', data=df_SiSSN, jitter=0.2, alpha=0.7, width_viol=0.5, width_box=0.1)
plt.xlabel('Block')
plt.ylabel('Genauigkeit')
plt.title('Raincloud Plot für Genauigkeit bei Block 1 & 2 (SiSSN)')
plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Festlegen der y-Achsenticks
plt.show()

# Raincloud-Plots für 'NV' und 'SiSSN' nebeneinander abbilden
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Raincloud-Plot für 'NV' erstellen
ax1 = pt.RainCloud(x='block', y='accu', data=df_NV, jitter=0.2, alpha=0.7, width_viol=0.5, width_box=0.1, ax=axes[0])
ax1.set_xlabel('Block')
ax1.set_ylabel('Genauigkeit')
ax1.set_title('Raincloud Plot für Genauigkeit bei Block 1 & 2 (NV)')
ax1.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Festlegen der y-Achsenticks

# Raincloud-Plot für 'SiSSN' erstellen
ax2 = pt.RainCloud(x='block', y='accu', data=df_SiSSN, jitter=0.2, alpha=0.7, width_viol=0.5, width_box=0.1, ax=axes[1])
ax2.set_xlabel('Block')
ax2.set_ylabel('Genauigkeit')
ax2.set_title('Raincloud Plot für Genauigkeit bei Block 1 & 2 (SiSSN)')
ax2.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Festlegen der y-Achsenticks

plt.tight_layout()  # Platz zwischen den Subplots einstellen
plt.show()

#%% Raincloud-Plot für noise 'NV'/'SiSSN' und 'position' 

# Raincloud-Plot für 'NV' erstellen
plt.figure(figsize=(10, 6))
ax1 = pt.RainCloud(x='position', y='accu', data=df_NV, jitter=0.2, alpha=0.7, width_viol=0.5, width_box=0.1)
plt.xlabel('Position')
plt.ylabel('Genauigkeit')
plt.title('Raincloud Plot für Genauigkeit der Position (NV)')
plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Festlegen der y-Achsenticks
plt.show()

# Raincloud-Plot für 'SiSSN' erstellen
plt.figure(figsize=(10, 6))
ax2 = pt.RainCloud(x='position', y='accu', data=df_SiSSN, jitter=0.2, alpha=0.7, width_viol=0.5, width_box=0.1)
plt.xlabel('Position')
plt.ylabel('Genauigkeit')
plt.title('Raincloud Plot für Genauigkeit der Position (SiSSN)')
plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Festlegen der y-Achsenticks
plt.show()

# Raincloud-Plots für 'NV' und 'SiSSN' nebeneinander abbilden
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Raincloud-Plot für 'NV' erstellen
ax1 = pt.RainCloud(x='position', y='accu', data=df_NV, jitter=0.2, alpha=0.7, width_viol=0.5, width_box=0.1, ax=axes[0])
ax1.set_xlabel('Position')
ax1.set_ylabel('Genauigkeit')
ax1.set_title('Raincloud Plot für Genauigkeit der Position (NV)')
ax1.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Festlegen der y-Achsenticks

# Raincloud-Plot für 'SiSSN' erstellen
ax2 = pt.RainCloud(x='position', y='accu', data=df_SiSSN, jitter=0.2, alpha=0.7, width_viol=0.5, width_box=0.1, ax=axes[1])
ax2.set_xlabel('Position')
ax2.set_ylabel('Genauigkeit')
ax2.set_title('Raincloud Plot für Genauigkeit der Position (SiSSN)')
ax2.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])  # Festlegen der y-Achsenticks

plt.tight_layout()  # Platz zwischen den Subplots einstellen
plt.show()

#%% Linien Plots

import seaborn as sns
import matplotlib.pyplot as plt

# Linien Plot erstellen für 'NV', 'block' und 'levels'
plt.figure(figsize=(10, 6))
sns.lineplot(x='block', y='accu', hue='levels', data=df_NV, marker='o')

# Plot anpassen
plt.xlabel('Block')
plt.ylabel('Genauigkeit')
plt.title('Linien Plot für Genauigkeit bei Block 1 & 2 (NV)')
plt.legend(title='Levels')
plt.grid(True)

# Setzen der x-Achsenbeschriftungen auf "Block 1" und "Block 2"
plt.xticks(df_NV['block'].unique(), ['Block 1', 'Block 2'])

plt.show()

# Linien Plot erstellen für für 'NV', 'block' und 'position'
plt.figure(figsize=(10, 6))
sns.lineplot(x='block', y='accu', hue='position', data=df_NV, marker='o')

# Plot anpassen
plt.xlabel('Block')
plt.ylabel('Accuracy')
plt.title('Linien Plot für Genauigkeit bei Block 1 & 2 (NV)')
plt.legend(title='Position')
plt.grid(True)

# Setzen der x-Achsenbeschriftungen auf "Block 1" und "Block 2"
plt.xticks(df_NV['block'].unique(), ['Block 1', 'Block 2'])

plt.show()

# Linien Plot erstellen für 'NV', 'position' und 'levels'

plt.figure(figsize=(10, 6))
sns.lineplot(x='position', y='accu', hue='levels', data=df_NV, marker='o')

# Plot anpassen
plt.xlabel('Position')
plt.ylabel('Genauigeit')
plt.title('Genauigkeit bei Position für Levels (NV)')
plt.legend(title='Levels')
plt.grid(True)

plt.show()

# Linien Plot erstellen für 'SiSSN', 'block' und 'levels'
plt.figure(figsize=(10, 6))
sns.lineplot(x='block', y='accu', hue='levels', data=df_SiSSN, marker='o')

# Linien Plot anpassen
plt.xlabel('Block')
plt.ylabel('Genauigkeit')
plt.title('Linien Plot für Genauigkeit bei Block 1 & 2 (SiSSN)')
plt.legend(title='Levels')
plt.grid(True)

# Setzen der x-Achsenbeschriftungen auf "Block 1" und "Block 2"
plt.xticks(df_SiSSN['block'].unique(), ['Block 1', 'Block 2'])

plt.show()

# Linien Plot erstellen für 'SiSSN', 'block' und 'position'
plt.figure(figsize=(10, 6))
sns.lineplot(x='block', y='accu', hue='position', data=df_SiSSN, marker='o')

# Plot anpassen
plt.xlabel('Block')
plt.ylabel('Genauigkeit')
plt.title('Linien Plot für Genauigkeit bei Block 1 & 2 (SiSSN)')
plt.legend(title='Position')
plt.grid(True)

# Setzen der x-Achsenbeschriftungen auf "Block 1" und "Block 2"
plt.xticks(df_SiSSN['block'].unique(), ['Block 1', 'Block 2'])

plt.show()

# Linien Plot erstellen für 'SiSSN', 'position' und 'levels'

# Plot erstellen
plt.figure(figsize=(10, 6))
sns.lineplot(x='position', y='accu', hue='levels', data=df_SiSSN, marker='o')

# Plot anpassen
plt.xlabel('Position')
plt.ylabel('Genauigkeit')
plt.title('Genauigkeit bei Position für Levels (NV)')
plt.legend(title='Levels')
plt.grid(True)

plt.show()

#%% Mittelwerte der einzelnen Subjekte 

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# NV: Gruppieren nach 'subj', 'levels' und Berechnen des Mittelwerts für 'accu'
mean_accu_by_subj_levels_NV = df_NV.groupby(['subj', 'levels'])['accu'].mean().reset_index()

# Streudiagramm erstellen
plt.figure(figsize=(10, 6))
sns.scatterplot(data=mean_accu_by_subj_levels_NV, x='levels', y='accu', hue='subj', palette='tab20', s=100)
plt.title('Mittelwerte von Genauigkeit für NV nach Subjekt und Levels')
plt.xlabel('Levels')
plt.ylabel('Mittelwert von Genauigkeit')
plt.legend(title='Subjekt', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Streudiagramm erstellen
plt.figure(figsize=(10, 6))
sns.scatterplot(data=mean_accu_by_subj_levels_NV, x='levels', y='accu', hue='subj', palette='tab20', s=100)

# Linien zwischen den Punkten desselben Subjekts zeichnen
for subj in mean_accu_by_subj_levels_NV['subj'].unique():
    data_subj = mean_accu_by_subj_levels_NV[mean_accu_by_subj_levels_NV['subj'] == subj]
    plt.plot(data_subj['levels'], data_subj['accu'], marker='o', linestyle='-', markersize=8)

plt.title('Mittelwerte von Genauigkeit für NV nach Subjekt und Levels')
plt.xlabel('Levels')
plt.ylabel('Mittelwert von Genauigkeit')
plt.legend(title='Subjekt', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# NV: Gruppieren nach 'subj', 'position' und Berechnen des Mittelwerts für 'accu'

mean_accu_by_subj_position_NV = df_NV.groupby(['subj', 'position'])['accu'].mean().reset_index()

# Streudiagramm erstellen
plt.figure(figsize=(10, 6))
sns.scatterplot(data=mean_accu_by_subj_position_NV, x='position', y='accu', hue='subj', palette='tab20', s=100)
plt.title('Mittelwerte von Genauigkeit für NV nach Subjekt und Position')
plt.xlabel('Levels')
plt.ylabel('Mittelwert von Genauigkeit')
plt.legend(title='Subjekt', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Streudiagramm erstellen
plt.figure(figsize=(10, 6))
sns.scatterplot(data=mean_accu_by_subj_position_NV, x='position', y='accu', hue='subj', palette='tab20', s=100)

# Linien zwischen den Punkten desselben Subjekts zeichnen
for subj in mean_accu_by_subj_position_NV['subj'].unique():
    data_subj = mean_accu_by_subj_position_NV[mean_accu_by_subj_position_NV['subj'] == subj]
    plt.plot(data_subj['position'], data_subj['accu'], marker='o', linestyle='-', markersize=8)

plt.title('Mittelwerte von Genauigkeit für NV nach Subjekt und Position')
plt.xlabel('Levels')
plt.ylabel('Mittelwert von Genauigkeit')
plt.legend(title='Subjekt', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


#%% SiSSN: Gruppieren nach 'subj', 'levels' und Berechnen des Mittelwerts für 'accu'

# NV: Gruppieren nach 'subj', 'levels' und Berechnen des Mittelwerts für 'accu'
mean_accu_by_subj_levels_SiSSN = df_SiSSN.groupby(['subj', 'levels'])['accu'].mean().reset_index()

# Streudiagramm erstellen
plt.figure(figsize=(10, 6))
sns.scatterplot(data=mean_accu_by_subj_levels_SiSSN, x='levels', y='accu', hue='subj', palette='tab20', s=100)
plt.title('Mittelwerte von Genauigkeit für SiSSN nach Subjekt und Levels')
plt.xlabel('Levels')
plt.ylabel('Mittelwert von Genauigkeit')
plt.legend(title='Subjekt', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Streudiagramm erstellen
plt.figure(figsize=(10, 6))
sns.scatterplot(data=mean_accu_by_subj_levels_SiSSN, x='levels', y='accu', hue='subj', palette='tab20', s=100)

# Linien zwischen den Punkten desselben Subjekts zeichnen
for subj in mean_accu_by_subj_levels_SiSSN['subj'].unique():
    data_subj = mean_accu_by_subj_levels_SiSSN[mean_accu_by_subj_levels_SiSSN['subj'] == subj]
    plt.plot(data_subj['levels'], data_subj['accu'], marker='o', linestyle='-', markersize=8)

plt.title('Mittelwerte von Genauigkeit für SiSSN nach Subjekt und Levels')
plt.xlabel('Levels')
plt.ylabel('Mittelwert von Genauigkeit')
plt.legend(title='Subjekt', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

#SiSSN: Gruppieren nach 'subj', 'position' und Berechnen des Mittelwerts für 'accu'

mean_accu_by_subj_position_SiSSN = df_SiSSN.groupby(['subj', 'position'])['accu'].mean().reset_index()

# Streudiagramm erstellen
plt.figure(figsize=(10, 6))
sns.scatterplot(data=mean_accu_by_subj_position_SiSSN, x='position', y='accu', hue='subj', palette='tab20', s=100)
plt.title('Mittelwerte von Genauigkeit für SiSSN nach Subjekt und Position')
plt.xlabel('Levels')
plt.ylabel('Mittelwert von Genauigkeit')
plt.legend(title='Subjekt', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# Streudiagramm erstellen
plt.figure(figsize=(10, 6))
sns.scatterplot(data=mean_accu_by_subj_position_SiSSN, x='position', y='accu', hue='subj', palette='tab20', s=100)

# Linien zwischen den Punkten desselben Subjekts zeichnen
for subj in mean_accu_by_subj_position_SiSSN['subj'].unique():
    data_subj = mean_accu_by_subj_position_SiSSN[mean_accu_by_subj_position_SiSSN['subj'] == subj]
    plt.plot(data_subj['position'], data_subj['accu'], marker='o', linestyle='-', markersize=8)

plt.title('Mittelwerte von Genauigkeit für SiSSN nach Subjekt und Position')
plt.xlabel('Levels')
plt.ylabel('Mittelwert von Genauigkeit')
plt.legend(title='Subjekt', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()


