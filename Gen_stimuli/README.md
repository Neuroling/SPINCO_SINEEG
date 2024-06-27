# Generation of Stimuli and Other Required Files

author: samuelmull

The scripts in these folders contain everything needed to generate the stimuli for the experiment, as well as any other files needed to run the experiment (i.e. the images for the selection screen, and the spreadsheets for stimulus presentation).

For a thorough pipeline, including what scripts need to be executed at what point, see `SINEEG/Docs/Procedures/Flowchart_stimuliGeneration_Experiment2.pdf`. Refer to that flowchart if possible. [^1]

For a description of the experiment(s), read the [README](../Experiment/SiN/README.md) file found at `SINEEG/Scripts/Experiment/SiN/README.md`

### Folder organisation
- The folders are numbered in order of execution.  
- Within each folder, you will find a README file and the scripts.
- Scripts starting with `Exp1_` or `Exp2_` have been written for experiment1 / experiment 2 and were not used in the other one.
    - However, scripts labelled `Exp2_` may be based on the ones for experiment1.
- Some scripts are not labelled with either `Exp1_` or `Exp2_`. These scripts were used in both.
- The number after the experiment-label signify the order of execution. [^2] 
- The order of execution for folders and scripts is important, because some scripts create files that are prerequisites for the following script.
    - However, some scripts are optional.
    - Scripts in which the order of execution is `00` are always optional.    
    - For better insight into prerequisites and optionalities, see `SINEEG/Docs/Procedures/Flowchart_stimuliGeneration_Experiment2.pdf`



[^1]: You can find `Flowchart_stimuliGeneration_Experiment1.png` in the same folder. I cannot guarantee the flowchart for **experiment1** is correct or complete, though (see below)   

[^2]: Because I (samuelmull) was not yet working on the Project when experiment1 was set up, I cannot guarantee the order of execution for **experiment1** is correct.   
    I can vouch for the correctness of the labels for **experiment2** however, because I made it.
