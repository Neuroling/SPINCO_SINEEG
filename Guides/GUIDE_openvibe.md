Documentation http://openvibe.inria.fr/tutorial-the-most-basic-openvibe-setup/ 

Software for BCI and real time EEG processing. 

Two main components: server and designer.  

 

Basic procedure  

 

 Openvibe gets data from the acquisition device (e.g., Biosemi) through the Acquisition Server and sends it to one or more clients (e.g., OpenViBE designer). Clients can be in a different machine on the same network.  

 

 

 

Our experiment 

Based on the documentation from R. Becker 

Preparation before experiment 

Create a folder for current measurement (e.g., Measurement_666) with two subfolders:  

Acquisition material". Contains copies of:  

All audio stimuli and .xlsx file referring to them (for PsychoPy) 

 Inpout32.h, inpoutx64.lib and inpoutx64.dll. These are necessary for the EEG markers 

Openvibe experiment file 'alpha_triggered.xml' file  (output will write individual mean & sd alpha ratios)  

"Output data" . 

 

OpenViBE designer 64bit 

Input settings 

Open the openViBE experiment .xml file ('alpha_triggered.xml') and set the path and file name of the output files in the boxes showed in the figure:  

 

Begin of the pipeline: 
Begin of the pipeline: 
End of the pipeline: 
"PATH-TO-YOUR-OUTPUT-DA Here, the 
raw EEG file is stored as an file. It is used if ycw want to 
replay the current gmy&scenario with the data of the a given 
participant. 
-Y Here, 
the EEG file is Stored as Brain Vision file. It is used to analyze the 
data on 
"PA -5 Here, 
the processed EEG file is stored as Brain Vision file. It is used to 
ana ze the data on 
 

 

Fixed settings 

The following settings should be already set in the experiment file and we should not change: 

山 当 : 当 も に 一 山 PO 」 も 山 面 ま 山 を を 当 に 0 ま ゴ LLJ 興 Oq 」 0 一 一 ま 元 に に の を 山 に 
OJ -0q5 、 aa 」 
 


 