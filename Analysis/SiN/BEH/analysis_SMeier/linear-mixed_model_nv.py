# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 15:08:48 2024

@author: sibme
"""

# Behavioral analysis
# Read gathered table
# Read gathered table, perform minor format adjustments

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

# File paths
thisScriptDir = os.getcwd()
baseDir = thisScriptDir[:thisScriptDir.find("Scripts")]
dirinput = os.path.join(baseDir + 'Data','SiN','analysis','beh','task-sin')
diroutput = os.path.join(baseDir + 'Data','SiN','analysis','beh','task-sin')

# Find file read data set 
fileinput =  [os.path.join(dirinput, f) for f in os.listdir(dirinput) if f.startswith('Gathered_')]
df = pd.read_csv(fileinput[0], index_col=None)

# Relabel noise levels
levelmapping = {'0.6p': '1_easy','0.4p': '2_mid','0.2p': '3_hard','-7db': '1_easy','-9db': '2_mid','-11db': '3_hard'}
df['levels'] = df['levels'].replace(levelmapping) 

 #  ---------------
print(' Table read with ' + str(len(df)) + ' rows and ' + str(len(df. columns)) + ' columns')
#show(df, scrollY="400px", scrollCollapse=True, paging=False)

# %% Transform to long

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

#%% Linear mixed models
# Defining variable types

# Define variable types ! 
categorical_vars = ["block", "noise", "levels","position","voice"] 
for col in categorical_vars:
    df_long_accu[col] = df_long_accu[col].astype("category")
    
#df_long_accu["block"] = df_long_accu["block"].astype("category")
#df_long_accu["noise"] = df_long_accu["noise"].astype("category")
#df_long_accu["levels"] = df_long_accu["levels"].astype("category")
#df_long_accu["accu"] = df_long_accu["accu"].astype("int")
#df_long_accu["position"] = df_long_accu["position"].astype("category")

df_long_accu.info() 

#%% Model including noise type - just for orientation. Note that the two noise types are distinct.

import statsmodels.api as sm
import statsmodels.formula.api as smf

# Specify models 
md = smf.mixedlm("accu ~  noise + levels + block", df_long_accu, groups = df_long_accu["subj"]) 
mdf = md.fit()
print(mdf.summary())

#%%
# Separate DataFrames für SiSSN und NV erstellen
df_nv = df_long_accu[df_long_accu['noise'] == 'NV'].copy()
df_sissn = df_long_accu[df_long_accu['noise'] == 'SiSSN'].copy()

# Modell für NV
md_nv = smf.mixedlm("accu ~ levels + position + block", df_nv, groups=df_nv["subj"])
mdf_nv = md_nv.fit()
print("Summary for NV Model:\n")
print(mdf_nv.summary())



#%%
import pandas as pd
# import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

#%% Überprüfung der Modellgüte für NV 

# Prüfen der Normalverteilung der Residuen für das NV-Modell
residuals_nv = mdf_nv.resid
qqplot_nv = sm.qqplot(residuals_nv, line='s')
plt.title('QQ-Plot der Residuen für NV-Modell')
plt.show()

from scipy.stats import shapiro

# Durchführung des Shapiro-Wilk-Tests für die Residuen des NV-Modells
statistic, p_value = shapiro(residuals_nv)
print("Shapiro-Wilk-Testergebnisse für NV-Modell:")
print("Teststatistik:", statistic)
print("p-Wert:", p_value)

# Interpretation des Ergebnisses
alpha = 0.05
if p_value > alpha:
    print("Die Residuen für das NV-Modell könnten normalverteilt sein (p-Wert > 0.05).")
else:
    print("Die Residuen für das NV-Modell sind nicht normalverteilt (p-Wert <= 0.05).")

#%% Bartlett-Test für Homoskedastizität

bartlett_test_nv = stats.bartlett(mdf_nv.fittedvalues, residuals_nv)
print("Bartlett's Test p-value for homoscedasticity (NV Model):", bartlett_test_nv.pvalue)

# Interpretation des Homoskedastizitätstests
alpha = 0.05
if bartlett_test_nv.pvalue < alpha:
    print("Homoskedasticity ist nicht gegeben (p-Wert < 0.05).")
else:
    print("Homoskedasticity ist gegeben (p-Wert >= 0.05).")

#%% Multikollinarität

# Berechnen der VIF-Werte für das NV-Modell
variables_nv = df_nv[['levels', 'position', 'block']]
vif_nv = {variable: variance_inflation_factor(variables_nv.values, i) for i, variable in enumerate(variables_nv.columns)}
print("VIF Values:", vif_nv)

#%% # Changing optimization method to 'bfgs' and increase in number of iterations
md_nv = smf.mixedlm("accu ~ levels + position + block", df_nv, groups=df_nv["subj"])
mdf_nv = md_nv.fit(method='bfgs', maxiter=1000)  
print(mdf_nv.summary())

#%% 5. AIC и BIC
aic = mdf_nv.aic
bic = mdf_nv.bic
print("AIC:", aic)
print("BIC:", bic)

# Überprüfung auf Linearität
# Plot beobachteten vs. vorhergesagten Werten
plt.figure()
plt.scatter(df_nv['accu'], mdf_nv.fittedvalues)
plt.xlabel('Beobachtete Werte')
plt.ylabel('Vorhergesagte Werte')
plt.title('Überprüfung der Linearität: Beobachtete vs. Vorhergesagte Werte für NV-Modell')
plt.show()

#%% Prüfung auf Unabhängigkeit der Residuen 
# Plot Residuen vs. vorhergesagten Werten
plt.figure()
plt.scatter(mdf_nv.fittedvalues, residuals_nv)
plt.xlabel('Vorhergesagte Werte')
plt.ylabel('Residuals')
plt.title('Prüfung auf Unabhängigkeit: Residuen vs. Vorhergesagte Werte')
plt.axhline(y=0, color='r', linestyle='--')
plt.show()

#%%
from sklearn.model_selection import KFold
# import numpy as np
import statsmodels.api as sm

# Folds number
n_splits = 5
kf = KFold(n_splits=n_splits)

# List of accuracy in a specific fold
cv_scores = []

# re-index df_nv because the indices are non-sequential
reIdx = pd.Series(range(len(df_nv)))
df_nv.set_index(reIdx, inplace = True)

# Splitting data 
for train_index, test_index in kf.split(df_nv):

    train_df = df_nv.iloc[train_index]
    test_df = df_nv.iloc[test_index]
    
    md_nv_split = smf.mixedlm("accu ~ levels + position + block", train_df, groups=train_df["subj"])
    mdf_nv_split = md_nv_split.fit()

    # Forecasting on test data
    y_pred = mdf_nv_split.predict(exog=test_df)

    # Quality of model assessment
    # Determination coefficient R^2 is used
    r_squared = np.corrcoef(test_df['accu'], y_pred)[0, 1] ** 2
    cv_scores.append(r_squared)

# Cross-validation results printing
print("Cross-Validation Scores:", cv_scores)

#%% Erkennung von Ausreissern

# Z-Score wird verwendet
from scipy import stats
df_nv['z_score_accu'] = np.abs(stats.zscore(df_nv['accu']))

# Löschung von Ausreißern
df_nv = df_nv[df_nv['z_score_accu'] < 3]

#%%
# Log transform of accu
df_nv['log_accu'] = np.log(df_nv['accu'] + 1)

# LMM results with log of accu
md_nv = smf.mixedlm("log_accu ~ levels + position + block", df_nv, groups=df_nv["subj"])
mdf_nv = md_nv.fit()
print("Summary for NV-Log-Model:\n")
print(mdf_nv.summary())

#%% Überprüfung der Modellgüte für NV-Log

# Prüfen der Normalverteilung der Residuen für das NV-Log-Modell
residuals_nv = mdf_nv.resid
qqplot = sm.qqplot(residuals_nv, line='s')
plt.title('QQ-Plot der Residuen für NV-Log-Modell')
plt.show()

from scipy.stats import shapiro

# Durchführung des Shapiro-Wilk-Tests für die Residuen des NV-Modells
statistic, p_value = shapiro(residuals_nv)
print("Shapiro-Wilk-Testergebnisse für NV-Log-Modell:")
print("Teststatistik:", statistic)
print("p-Wert:", p_value)

# Interpretation des Ergebnisses
alpha = 0.05
if p_value > alpha:
    print("Die Residuen für das NV-Modell könnten normalverteilt sein (p-Wert > 0.05).")
else:
    print("Die Residuen für das NV-Modell sind nicht normalverteilt (p-Wert <= 0.05).")

#%% Überprüfung auf Linearität
# Plot beobachteten vs. vorhergesagten Werten
plt.figure()
plt.scatter(df_nv['log_accu'], mdf_nv.fittedvalues)
plt.xlabel('Beobachtete Werte')
plt.ylabel('Vorhergesagte Werte')
plt.title('Überprüfung der Linearität: Beobachtete vs. Vorhergesagte Werte für NV-Log-Modell')
plt.show()


#%%#%% Prüfung auf Unabhängigkeit der Residuen 
# Plot Residuen vs. vorhergesagten Werten

plt.figure()
plt.scatter(mdf_nv.fittedvalues, residuals_nv)
plt.xlabel('Vorhergesagte Werte')
plt.ylabel('Residuals')
plt.title('Prüfung auf Unabhängigkeit: Residuen vs. Vorhergesagte Werte für NV-Log-Modell')
plt.axhline(y=0, color='r', linestyle='--')
plt.show()


#%% Multikollinarität
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Extract independent variables for the model
variables_nv = df_nv[['levels', 'position', 'block']]

# Calculate VIF for each variable
vif_nv = {variable: variance_inflation_factor(variables_nv.values, i) for i, variable in enumerate(variables_nv.columns)}

# Output VIF values
print("VIF Values for NV Model:", vif_nv)






