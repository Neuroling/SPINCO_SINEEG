# EEG test in science cluster
Here we just want to read raw EEG data with two different tools: matlab-based EEGlab and python-based MNE. Then, matlab-based AUTOMAGIC is used for standradized preprocessing pipeline (EEGlab-functions)


1. Python and MNE
Organizes the data in BIDS format by creating .json metadatafiles . For reading things like file duration and sampling rate it uses MNE to import the raw data set and extract this info. 


2. EEGlab  (Matlab)
Imports bdf, reads channel location file and saves downsampled dataset as eeglab .set file


3. EEGlab and Automagic (Matlab)
The Automagic toolbox for standardized, automated preprocessing pipelines relies heavily on a GUI. But it is possible to create and run a project from commandline seems to work. 

> Issues
 > - [ ] Uses Parpool 
> - [ ] Tends to produce hard to trace errors and warnings since it calls  a mix of its own functions and eeglab functions
> - [ ] EEGlab pop ups (ICA 'interrupt' window)
> - [ ] Automagic pops up main panel at the end 


## Terminology

- **SSH or Secure Shell**
 is a network communication protocol that enables two computers to communicate (c.f http or hypertext transfer protocol, which is the protocol used to transfer hypertext such as web pages) and share data
 
