# Automagic prefixes
Preprocessing done with Automagic 

https://github.com/methlabUZH/automagic/wiki/Quality-Assessment-and-Rating


## Outputs 
For each preprocessed dataset, a jpg. file is saved (in the same folder), providing a visual representation of the effects of the applied preprocessing methods.6 In addition, a log-file is saved for each dataset, describing the exact order and the used parameters of the preprocessing steps. This logfile can be used to precisely communicate the preprocessing of an EEG project in a publication in accordance with the recommendation for reporting standards of the Committee on Best Practice in Data Analysis and Sharing (COBIDAS) (Pernet et al., 2018).

### Combination of File Prefixes

np - preprocessed file not rated (no channels to interpolate / interpolated) 

gp - preprocessed file rated as Good (no channels to interpolate / interpolated)

op - preprocessed file rated as OK (no channels to interpolate / interpolated)

bp - preprocessed file rated as Bad (no channels to interpolate / interpolated)

ip - preprocessed file some electrodes to interpolate or have been interpolated

gip - preprocessed file rated as Good and interpolated at least once

oip - preprocessed file rated as OK and interpolated at least once

bip - preprocessed file rated as Bad and interpolated at least once

ip - preprocessed file rated as Interpolated and interpolated at least once

Examples for Multiple Commits:

ggiip - committed twice, the rating remained

goiip - committed twice, the rating changed from ok to good

### "reduced_" files
Users may have observed a reduced_*.mat file in the results folders. This file is a downsampled version of the EEG data and is used for faster displaying in the data viewer.
