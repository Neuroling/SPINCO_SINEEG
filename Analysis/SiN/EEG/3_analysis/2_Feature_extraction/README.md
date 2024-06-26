# Feature Extraction

author: samuelmull

### Folder Organisation

**2_Feature_extraction** folder is for all scripts that deal with the extraction of frequency features from the epoched data, using time frequency representations (TFR)

- **FeatureExtraction_runner.py** is the main script for finished code   
- **FeatureExtraction_functions.py** is a collection of functions for handling epoching   
- **FeatureExtraction_constants.py** contains variables that do not change across files, such as subject IDs   
- **sketch_FeatureExtraction_writing.py** is for trying out and debugging code before putting it in FeatureExtraction_functions.py   


### Package Requirements

[mne](https://mne.tools/stable/install/index.html)   
Some plotting functions of mne are bugged in matplotlib version 3.7.2 and earlier. Update matplotlib to at least 3.7.3 to ensure smooth operation.


### Issue: Dealing with a frozen kernel

If `n_jobs = -1` (in the constants), there's a risk of the kernel getting killed mid-execution of the runner-script due to running out of RAM.  
Try one or more of the following:  
    - In the constants, set `n_jobs = None` (sequential processing. Will take longer)
    - In the constants, set `decim = 2` (or higher if necessary. This will decimate the sampling rate.)
    - Instead of looping over subjects, manually run the code for each subject. Open a new console for every subject.
  
## Background Information
### Wavelet Width, Cycles and Frequencies

Paraphrased from [here](https://mne.tools/stable/generated/mne.time_frequency.morlet.html#mne.time_frequency.morlet)  

The width of a wavelet is determined by `Sigma`, which is the standard deviation of the Gaussian envelope.   
The wavelet extends to +/-5 standard deviations, so the values at tail ends are close to 0.   
`Sigma` is determined by `freqs` and `n_cycles`:   
```
sigma = n_cycles/(2 * np.pi * freqs)
```

In other words:  
- `(2 * np.pi * freqs)` = one completed sine-wave of `freqs` (= one cycle)  
- Therefore: `n_cycles` determines how many cycles are in a standard deviation of the gaussian envelope  
- Higher `n_cycles` will give a higher `sigma` and therefore a broader wavelet  


if `n_cycles = freqs / 2` then `sigma` will always be `= 1 / (4 * np.pi) = 0.079577`  
⇒ and that is why you don't want to make `n_cycles` dependent on `freqs`  


### Cone Of Influence (COI)

For the Cone of Influence, we use the **full width at half maximum (FWHM)**.   
It is defined as the window between when the gaussian envelope is at 50% before and after the peak.   

The full-width half-maximum (FWHM) can be determined by:    
`fwhm = sigma * 2 * np.sqrt(2 * np.log(2))`   
    or   
`fwhm = n_cycles * np.sqrt(2 * np.log(2))/(np.pi * freqs)`  
    
Consequently, the FWHM is approximately `2.355 * sigma`    
We use half of that for the COI on either side, so `1.173 * sigma`  
This is also called the **half width at half maximum (HWHM)**  

Therefore:  
- For the COI, we want to exclude data outside of the HWHM on the first and last wavelet.  
- Our wavelets extend to +/- 5 `sigma` on either side of the peak. 
    - Reminder: `sigma` is dependent on the frequency `(freqs`) and `n_cycles`
- This means that the first peak is at 5 `sigma`. The HWHM of that peak is therefore at 5-1.173 `sigma`.
- So we need to exclude values before `time[0] + ((5 - 1.173) * sigma)` and after `time[-1] - ((5 - 1.173) * sigma)`  
    
In other words:  
- `n_cycles` determines how many complete cycles in a given frequency (`freqs`), multiplied by 3.27 (= 5 - 1.173) are at the boundary of the COI.
