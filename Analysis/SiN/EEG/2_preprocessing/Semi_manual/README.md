This pipeline is intended for a manual data quality inspection. Later this can be compared to the automagic pipeline. Involves:

- Inspect and log bad channels
- Inspect and mark bad data segments
- Run ICA with labels and confirm/ inspect components 

The Tutorial from the EEGlab Wiki is used as main source: 
https://eeglab.org/tutorials/06_RejectArtifacts/



# Steps
## 0. Prepare your data folder
Keep raw data safe:
Copy the relevant raw data files (note per dataset there are two files .fdt and .set)  to your preprocessing folder.

## 1. Before inspection 

- First, let's remove channel with Audiosignal (channel 71)

### 1.1 Filter
- Basic FIR filter: hight pass 0.5 hz 
- Notch (slow)Uses extension CleanLine: select line noise to remove: 50 hz]
- Remove channel with Audiosignal (channel 71)

### 1.2 Re-reference 
- Cz: see  https://eeglab.org/tutorials/05_Preprocess/rereferencing.html 

### 1.3 Resample
- Downsample to e.g. 128  

## 2. Visual Inspection 
- First look for bad channels
- Look for bad data periods and mark them 
-
