# Preprocessing 

## Pipeline from T. Houweling
* \[Script: DiN_pt01_preprocess_segment01.m]
  1. Import data (raw)
  2. Add channel locations and measurement unit
  3. Downsample (from 2kHz to 200Hz)
  4. Filter (highpass: 0.1Hz, lowpass: 48Hz)
  5. Remove line noise
  6. Remove bad channels & data segments
  7. Interpolate the removed channels
  8. Re-reference to average

* \[Script: DiN_pt01_preprocess_segment02.m]
  This script merges .set files resulting in one dataset per subject
  
* \[Script: DiN_pt01_preprocess_segment03.m]
  
  9.  Checks data consistency
  10. Epoch
  11. Reject noisy epochs
  12. Remove trials with no responses
  13. Runs ICA and rejects non-brain components
  
