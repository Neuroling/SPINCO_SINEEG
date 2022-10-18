# Openvibe

Documentation http://openvibe.inria.fr/tutorial-the-most-basic-openvibe-setup/ 
Software for BCI and real time EEG processing. 
Two main components: server and designer.  

## Basic procedure  

 Openvibe gets data from the acquisition device (e.g., Biosemi) through the Acquisition Server and sends it to one or more clients (e.g., OpenViBE designer). Clients can be in a different machine on the same network.  

 ## Our experiment 

Based on the documentation from R. Becker:

#### Preparation before experiment 
- Create a folder for current measurement (e.g., Measurement_666) with two subfolders:  
- Acquisition material". Contains copies of:  
      - All audio stimuli and .xlsx file referring to them (for PsychoPy) 
      -  Inpout32.h, inpoutx64.lib and inpoutx64.dll. These are necessary for the EEG markers 
      -  Openvibe experiment file 'alpha_triggered.xml' file  (output will write individual mean & sd alpha ratios)  "Output data" . 

## OpenViBE designer 64bit 
### Input settings 
Open the openViBE experiment .xml file ('alpha_triggered.xml') and set the path and file name of the output files in the boxes showed in the figure:  
 
 ![image](https://user-images.githubusercontent.com/13642762/196431435-4445f86b-70c8-4cfc-bb38-0d3f230b5cdd.png)

### Fixed settings 
The following settings should be already set in the experiment file and we should not change: 

![image](https://user-images.githubusercontent.com/13642762/196431745-e895ece6-8664-4884-80c4-f26180d7bd65.png)

 
