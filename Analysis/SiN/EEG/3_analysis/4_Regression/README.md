# Notes from Sam

## What to save from the LogReg Models
- `AIC`
- `coefs`
- `family`
- `fixef`
- `formula`
- `logLike`
- `ranef`
- `ranef_corr`
- `ranef_var`
- `sig_type`
- `warnings`

## Explanation of the formulas

### Syntax
See [this great explanation by Maarten Speekenbrink](https://mspeekenbrink.github.io/sdam-r-companion/linear-mixed-effects-models.html#formulating-and-estimating-linear-mixed-effects-models-with-lme4)

'accuracy ~ RT'
Will give us:
- A global intercept
- An estimate of the effect (slope) of RT on accuracy
Note: We do not actually use reaction time (RT) for our models, but I wanted a simple, non-categorial variable as example

'accuracy ~ RT + (1|subjID)'
Random Intercept Model. Will give us:
- All of the above
- Random effect intercepts for subjID. In other words: for each subjID, how their intercept deviates from the global intercept. It is assumed the subjIDs all have the same slope

'accuracy ~ eeg_data + (eeg_data|channel)'
Random Intercept and Slope Model. Will give us:
- Global intercept
- Global estimate of the effect of eeg_data on accuracy.
- Random effect intercepts for each unique channel
- Random effect (slopes) of eeg_data within each unique channel - or, more specifically, the degree to which the effect of eeg_data of a channel deviates from the global effect of eeg_data
- The correlations between the effect deviations and the intercept deviations between channels.  
This model is equivaluent to 'accuracy ~ eeg_data + (1 + eeg_data|channel)'

'accuracy ~ eeg_data + (eeg_data|channel:timeBin)'
Random Intercept and Slope Model. Will give us:
- All of the above but instead of "unique channel" it is every unique combination of channel and timeBin.
- Will not give us the intercept or slope of every unique channel across timeBins nor of every unique timeBin across channels

'accuracy ~ eeg_data + (eeg_data|channel/timeBin)'
Random Intercept and Slope Model. Will give us:
- Same as the above but this will also give us the intercept and slope of every unique channel.  
This model is equivalent to 'accuracy ~ eeg_data + (eeg_data|channel:timeBin) + (eeg_data|channel)'


### Specific formulas

'accuracy ~ 1 + (1|timeBin:channel)  + (1|subjID)'
Unconditional Model. Will give us 
- the variance in accuracy between subjects 
- the variance in accuracy between every unique combination of timeBin and channel (64*8 = 512 unique combinations).
