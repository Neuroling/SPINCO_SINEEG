# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 18:11:41 2024

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
dirinput = os.path.join(baseDir + 'a','Data','SiN','analysis','beh','task-sin')
diroutput = os.path.join(baseDir + 'a','Data','SiN','analysis','beh','task-sin')

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

#%% Separate DataFrames für SiSSN und NV erstellen
df_nv = df_long_accu[df_long_accu['noise'] == 'NV'].copy()
df_sissn = df_long_accu[df_long_accu['noise'] == 'SiSSN'].copy()

# Modell für NV
md_sissn = smf.mixedlm("accu ~ levels + position + block", df_sissn, groups=df_sissn["subj"])
mdf_sissn = md_sissn.fit()
print("Summary for NV Model:")
print(mdf_sissn.summary())

#%%
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
from scipy import stats
from statsmodels.stats.outliers_influence import variance_inflation_factor

#%% Überprüfung der Modellgüte für NV 

# Prüfen der Normalverteilung der Residuen für das NV-Modell
residuals_sissn = mdf_sissn.resid
qqplot_sissn = sm.qqplot(residuals_sissn, line='s')
plt.title('QQ-Plot der Residuen für SiSSN-Modell')
plt.show()

from scipy.stats import shapiro

# Durchführung des Shapiro-Wilk-Tests für die Residuen des NV-Modells
statistic, p_value = shapiro(residuals_sissn)
print("Shapiro-Wilk-Testergebnisse für NV-Modell:")
print("Teststatistik:", statistic)
print("p-Wert:", p_value)

# Interpretation des Ergebnisses
alpha = 0.05
if p_value > alpha:
    print("Die Residuen für das SiSSN-Modell könnten normalverteilt sein (p-Wert > 0.05).")
else:
    print("Die Residuen für das SiSSN-Modell sind nicht normalverteilt (p-Wert <= 0.05).")

#%% Bartlett-Test für Homoskedastizität

bartlett_test_sissn = stats.bartlett(mdf_sissn.fittedvalues, residuals_sissn)
print("Bartlett's Test p-value for homoscedasticity (SiSSN Model):", bartlett_test_sissn.pvalue)

# Interpretation des Homoskedastizitätstests
alpha = 0.05
if bartlett_test_sissn.pvalue < alpha:
    print("Homoskedasticity ist nicht gegeben (p-Wert < 0.05).")
else:
    print("Homoskedasticity ist gegeben (p-Wert >= 0.05).")

#%% Multikollinarität

# Berechnen der VIF-Werte für das NV-Modell
# variables_sissn = df_sissn[['levels', 'position', 'block']]
# vif_sissn = {variable: variance_inflation_factor(variables_sissn.values, i) for i, variable in enumerate(variables_sissn.columns)}
# print("VIF Values:", vif_sissn)

#%% # Changing optimization method to 'bfgs' and increase in number of iterations
md_sissn = smf.mixedlm("accu ~ levels + position + block", df_sissn, groups=df_sissn["subj"])
mdf_sissn = md_sissn.fit(method='bfgs', maxiter=1000)  
print(mdf_sissn.summary())

#%% 5. AIC и BIC
aic = mdf_sissn.aic
bic = mdf_sissn.bic
print("AIC:", aic)
print("BIC:", bic)

# Überprüfung auf Linearität
# Plot beobachteten vs. vorhergesagten Werten
plt.figure()
plt.scatter(df_sissn['accu'], mdf_sissn.fittedvalues)
plt.xlabel('Beobachtete Werte')
plt.ylabel('Vorhergesagte Werte')
plt.title('Überprüfung der Linearität: Beobachtete vs. Vorhergesagte Werte für SiSSN-Modell')
plt.show()

#%% Prüfung auf Unabhängigkeit der Residuen 
# Plot Residuen vs. vorhergesagten Werten
plt.figure()
plt.scatter(mdf_sissn.fittedvalues, residuals_sissn)
plt.xlabel('Vorhergesagte Werte')
plt.ylabel('Residuals')
plt.title('Prüfung auf Unabhängigkeit: Residuen vs. Vorhergesagte Werte')
plt.axhline(y=0, color='r', linestyle='--')
plt.show()

#%%
from sklearn.model_selection import KFold
import numpy as np
import statsmodels.api as sm

# Folds number
n_splits = 5
kf = KFold(n_splits=n_splits)

# List of accuracy in a specific fold
cv_scores = []

# Splitting data 
for train_index, test_index in kf.split(df_sissn):
    X_train, X_test = df_sissn.loc[train_index, ['levels', 'position', 'block']], df_sissn.loc[test_index, ['levels', 'position', 'block']]
    y_train, y_test = df_sissn.loc[train_index, 'accu'], df_sissn.loc[test_index, 'accu']

    md_sissn = sm.MixedLM(endog=y_train, exog=X_train, groups=df_sissn.loc[train_index, 'subj'])
    mdf_sissn = md_sissn.fit()

    # Forecasting on test data
    y_pred = mdf_sissn.predict(exog=X_test)

    # Quality of model assessment
    # Determination coefficient R^2 is used
    r_squared = np.corrcoef(y_test, y_pred)[0, 1] ** 2
    cv_scores.append(r_squared)

# Cross-validation results printing
print("Cross-Validation Scores:", cv_scores)

#%% Erkennung von Ausreissern

# Z-Score wird verwendet
from scipy import stats
df_sissn['z_score_accu'] = np.abs(stats.zscore(df_sissn['accu']))

# Löschung von Ausreißern
df_sissn = df_sissn[df_sissn['z_score_accu'] < 3]

#%%
# Log transform of accu
df_sissn['log_accu'] = np.log(df_sissn['accu'] + 1)

# LMM results with log of accu
md_sissn = smf.mixedlm("log_accu ~ levels + position + block", df_sissn, groups=df_sissn["subj"])
mdf_sissn = md_sissn.fit()
print(mdf_sissn.summary())

#%% Überprüfung der Modellgüte für SiSSN-Log

# Prüfen der Normalverteilung der Residuen für das SiSSN-Log-Modell
residuals_sissn = mdf_sissn.resid
qqplot = sm.qqplot(residuals_sissn, line='s')
plt.title('QQ-Plot der Residuen für SiSSN-Log-Modell')
plt.show()

from scipy.stats import shapiro

# Durchführung des Shapiro-Wilk-Tests für die Residuen des NV-Modells
statistic, p_value = shapiro(residuals_sissn)
print("Shapiro-Wilk-Testergebnisse für SiSSN-Log-Modell:")
print("Teststatistik:", statistic)
print("p-Wert:", p_value)

# Interpretation des Ergebnisses
alpha = 0.05
if p_value > alpha:
    print("Die Residuen für das SiSSN-Modell könnten normalverteilt sein (p-Wert > 0.05).")
else:
    print("Die Residuen für das SiSSN-Modell sind nicht normalverteilt (p-Wert <= 0.05).")

#%% Überprüfung auf Linearität
# Plot beobachteten vs. vorhergesagten Werten
plt.figure()
plt.scatter(df_sissn['log_accu'], mdf_sissn.fittedvalues)
plt.xlabel('Beobachtete Werte')
plt.ylabel('Vorhergesagte Werte')
plt.title('Überprüfung der Linearität: Beobachtete vs. Vorhergesagte Werte für SiSSN-Log-Modell')
plt.show()


#%%#%% Prüfung auf Unabhängigkeit der Residuen 
# Plot Residuen vs. vorhergesagten Werten

plt.figure()
plt.scatter(mdf_sissn.fittedvalues, residuals_sissn)
plt.xlabel('Vorhergesagte Werte')
plt.ylabel('Residuals')
plt.title('Prüfung auf Unabhängigkeit: Residuen vs. Vorhergesagte Werte für SiSSN-Log-Modell')
plt.axhline(y=0, color='r', linestyle='--')
plt.show()

#%% Multikollinarität
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Extract independent variables for the model
variables_sissn = df_sissn[['levels', 'position', 'block']]

# Calculate VIF for each variable
vif_sissn = {variable: variance_inflation_factor(variables_sissn.values, i) for i, variable in enumerate(variables_sissn.columns)}

# Output VIF values
print("VIF Values for NV Model:", vif_sissn)