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

# Science IT Services
Don't know whether to use science Cloud or science Cluster? check  https://www.zi.uzh.ch/en/teaching-and-research/science-it/computing.html
see proper manual in : https://docs.s3it.uzh.ch/cluster/cluster_training 

![image](https://github.com/Neuroling/SPINCO_SINEEG/assets/13642762/bed0cdbb-9daa-4996-93fe-162b88a9ab11)

ScienceCloud
- Offers Virtual Machines that are controlled by the user
- Great for interactive use
- The user has root (sudo) privileges and can customize system software
- Multiple operating systems are available: Ubuntu Linux or another Linux distribution

ScienceCluster
- A shared cluster environment with compute resources managed by SLURM
- Great for large batches of jobs (up to thousands jobs submitted at a time)
- A user can install software only in their user directories, and commonly-used software is maintained by Science IT
- Only one operating System is available: Ubuntu Linux


# Quick tour on ScienceCluster 
See this for a proper manual: https://docs.s3it.uzh.ch/cluster/overview/
- **Connect** to the cluster via ssh with UZH shortname ssh shortusername@cluster.s3it.uzh.ch
> How does this work from WIndows terminal, need software? 

- **Data Storage** . Here there are 4 systems with different capacities BUT non of them has BACKUPS https://docs.s3it.uzh.ch/cluster/data/#scalable-storage 
- **Data Transfer** we can trasnfer files with the `scp` command to, for instance, copy files from a server to the cluster
- **Schedule Jobs**. They are submitted with the `sbatch` command. `Slurm` is the system for automatic job allocations. 

# User Example
Set up Slurm parameter 
```
ssh shortusername@cluster.s3it.uzh.ch

``` 

# Terminology
Just some rough non-technical definitions to get oriented

- **shell (sh)** . Shell is a computer program that exposes an operating system's services to a human user or other programs. It is named a shell because it is the outermost layer around the operating system.
-  **bash** . Bash is sh, but with more features and better syntax. Bash is “Bourne Again SHell”, and is an improvement of the sh (original Bourne shell). Shell scripting is scripting in any shell, whereas Bash scripting is scripting specifically for Bash. sh is a shell command-line interpreter of Unix/Unix-like operating systems. sh provides some built-in commands. bash is a superset of sh. Shell is a command-line interface to run commands and shell scripts. Shells come in a variety of flavors, much as operating systems come in a variety of flavors. So, Shell is an interface between the user and the operating system, which helps the user to interact with the device.
- **SSH or Secure Shell**
 is a network communication protocol that enables two computers to communicate (c.f http or hypertext transfer protocol, which is the protocol used to transfer hypertext such as web pages) and share data. The stuff 
- **Slurm** manages and schedules jobs in the  cluster. Stands for the Simple Linux Utility for Resource Management (Slurm Workload Manager)  
 
