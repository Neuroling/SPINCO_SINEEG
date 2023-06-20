
# Quick tour on ScienceCluster 
Documentation:  https://docs.s3it.uzh.ch/cluster/overview/

In the cluster we can: 
- *Connect* to the cluster via ssh with UZH shortname ssh shortusername@cluster.s3it.uzh.ch
- *Data Storage* . Here there are 4 systems with different capacities BUT non of them has BACKUPS https://docs.s3it.uzh.ch/cluster/data/#scalable-storage 
- *Data Transfer* we can transfer files with the `scp` command to, for instance, copy files from a server to the cluster
- *Schedule Jobs*. They are submitted with the `sbatch` command. `Slurm` is the system for automatic job allocations. 

# Example 1: using MNE-python toolbox
We may be running multiple projects in the cluster. This section is based on: https://docs.s3it.uzh.ch/cluster/overview/ 
## Login
In our cluster space there will be 3 directories in our 'home': *data*, *scratch* and the *shares* directory assigned to the specific project. In 'shares' we can search for our project, e.g. *hervais-adelman.lizz.uzh*

### Login from ScienceApps
Go here and log in: 
https://apps.s3it.uzh.ch/
### Login from terminal
Type  ```ssh shortname@cluster.s3it.uzh.ch``` with your uzh shortname. You will be asked for password. Then you will see message and a table showing your directories and their available space 

## Creating a Python environment  
- Log in:
  ```
  ssh gfraga@cluster.s3it.uzh.ch
  ```
- Load mamba module:
  ```
  module load mamba
  ```
- Create enviroment: For example to create an enviroment with mne and other toolboxes. I name it *SINEEG-env*:
  ```bash
  conda create --strict-channel-priority --channel=conda-forge --name=SINEEG-env mne-base h5io h5py pymatreader mne-bids matplotlib scikit-learn
  
  ```
- The new enviroment will be saved in `/home/gfraga/data/conda/envs/` This is the default, recommended location (this could be modified by changing the .condarc file:  https://docs.s3it.uzh.ch/how-to_articles/how_to_use_conda/)
  
- Activate enviroment :
  ```
  conda activate SINEEG-env
  ```
- To get out of the environment: ``` conda deactivate ```
- To delete an environment: ```` conda remove --name SINEEG-env --all ````
 

## Accessing data 

### Link to your project 'shares' folder
 Do this to create a link to your project (e.g,m *shares* 
 ```
 ln -s /shares/hervais-adelman.lizz.uzh ~/shares
```
### Access to SMB NAS (mounted drives)
In this case we have data and scripts in our **NAS** `\\idnas12.d.uzh.ch\G_PSYNEULIN_DATA$ `
The script uses relative paths to access data, summing Scripts and Data are children of a parent "Project" directory: PROJECT/data and PROJECT/Scripts

Here we will try 
- Access SMB share from the Science Cluster
  `smbclient --max-protocol SMB3 -W UZH -U username nasaddress` 
  ```shell
  smbclient --max-protocol SMB3 -W UZH -U gfraga //idnas12.d.uzh.ch/G_PSYNEULIN_DATA$
  ```
- Now the terminal prompt will change to `smb: \>` and if we type 'dir' we will see the content of our smb server.
- If we want out we can type `exit` and we will go back to the usual login prompt 'gfraga@...'

## Creating the job 
We first create a file with some bash script (Here the first line creates the .sh file with the subsequent lines).
````bash
cat << EOF > helloscript.sh
#!/bin/bash
#SBATCH --job-name=arrayJob
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=4GB
#SBATCH --output=arrayJob_%A_%a.out
#SBATCH --error=arrayJob_%A_%a.err
#SBATCH --array=1-3

module load mamba
source activate renv
# Print this sub-job's task ID
echo "My SLURM_ARRAY_TASK_ID: " \$SLURM_ARRAY_TASK_ID
srun Rscript --vanilla Hello.py \$SLURM_ARRAY_TASK_ID
EOF

````


### 
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

<img src="https://github.com/Neuroling/SPINCO_SINEEG/assets/13642762/bed0cdbb-9daa-4996-93fe-162b88a9ab11" width="650" height="350">

**ScienceCloud**
- Offers Virtual Machines that are controlled by the user
- Great for interactive use
- The user has root (sudo) privileges and can customize system software
- Multiple operating systems are available: Ubuntu Linux or another Linux distribution

**ScienceCluster**
- A shared cluster environment with compute resources managed by SLURM
- Great for large batches of jobs (up to thousands jobs submitted at a time)
- A user can install software only in their user directories, and commonly-used software is maintained by Science IT
- Only one operating System is available: Ubuntu Linux


  
## Project set up
Set up Slurm parameter to sbatch in the **command line**:
```
--account=hervais-adelman.lizz.uzh
```
OR we add this line to the **slurm script**:
```
#SBATCH --account= hervais-adelman.lizz.uzh
```
Without the account setting, your job will be charged under your default project, which is not this one (the default project can be changed)

## Connect to cluster 
We use our UZH shortname. If we are unable to log in our email /collaboration password will need to be updated in the Identity manager: https://identity.uzh.ch/itim/ui/

```
ssh shortusername@cluster.s3it.uzh.ch
```
## Data storage and access 
If we have data in a UZH mounted NAS (network attached storage): https://docs.s3it.uzh.ch/how-to_articles/how_to_access_uzh_nas_with_smbclient/
We need this command:
```
smbclient --max-protocol SMB3 -W UZH -U uzhshortname //nasaddress
```
nassaddress is the address to our NAS: \\idnas12.d.uzh.ch\G_PSYNEULIN_DATA$ 
If this works we will be prompted to enter our password 
Here we have operations with commands like `ls`,`cd`,`get` (download),`put` (upload),`exit`,    

Example of operation: 
```
smb: \> get test.txt new_test.txt
```
Copy test.txt to our ScienceCluster 

or 

```
smb: \> put new\_test.txt augmented\_test.txt
```
Upload a file from ScienceCluster to the NAS device


# Terminology
Just some rough non-technical definitions to get oriented

- **shell (sh)** . Shell is a computer program that exposes an operating system's services to a human user or other programs. It is named a shell because it is the outermost layer around the operating system. See bash:
-  **bash** . Bash is sh, but with more features and better syntax. Bash is “Bourne Again SHell”, and is an improvement of the sh (original Bourne shell). Shell scripting is scripting in any shell, whereas Bash scripting is scripting specifically for Bash. sh is a shell command-line interpreter of Unix/Unix-like operating systems. sh provides some built-in commands. bash is a superset of sh.
- **SSH or Secure Shell** is a network communication protocol that enables two computers to communicate (c.f http or hypertext transfer protocol, which is the protocol used to transfer hypertext such as web pages) and share data. 
- **Slurm** manages and schedules jobs in the  cluster. Stands for the Simple Linux Utility for Resource Management (Slurm Workload Manager)  
 
