# current QUERIES for Science Cloud  
- [x]  Linux graphic environment: accessibility, security
- [x] sharing snapshots between projects
 
# Linux VM with graphical environment
This approach uses the interface provided in the browser by the Science cloud. It has potential safety vulnerabilities as involves creating a user with a password so access would be possible without ssh key

## 1. Set up ssh key
See the 'Getting access to my VM' of the training material: https://docs.s3it.uzh.ch/cloud/training/training_handout/
It is likely you need to install Openssh feature for Windows(https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell#install-openssh-for-windows)
I had to install it copying the commands for powershell (up to the section connect to Open SSH server, excluding that) 

Once done go to power shell. In short: 
Go to windows `*powershell*`
- You will `ssh-keygen -t rsa -b 4096` to generate a key. Go with the defaults and it will save some files in your home directory .ssh
- From those files you will need to copy the public Key in the VM instance. So type  `cat ~/.ssh/id_rsa.pub` and copy the entire output. Go to the *Cloud dashboard* and paste it into the import KEY options of *Access and security*
- Then do `ssh -i ~/.ssh/id_rsa ubuntu@<your-instance-ip-address>` to access it. Get the IP from the cloud dashboard
- Next time you can just do `ssh ubuntu@<your-instance-ip-address>`

Now you are in the VM! 

Note: You can add several ssh keys to a VM

## 2. Updates and upgrades
> **IMPORTANT NOTE** 
It is the responsability the user to keep the VM up to date! some of the regular updates may be critical

- `sudo apt update` 
- `sudo apt upgrade`
- Critical updates will be regular. This process will have to be done regularly when working on the VM. It needs maintainance  constant `sudo unattended-upgrade`

## 3. Install Mate-minimal 
- `sudo apt install tasksel`
- `sudo tasksel` and select Mate-minimal (use arrow keys and spacebar to select, press tab to go to the OK button)  

## 4. Create user 
 > **IMPORTANT SAFETY NOTE **
 
- Install `sudo apt install fail2ban` to block it when someone puts the password wrong 3 times. 
- `sudo adduser <yourusername>`
- Give a SECURE password! min 16 characters combination of letters, numbers and symbols...
- Ignore other details if you wish (press Enter in the upcoming queries

## 5. User Access to desktop environment
### 5.1. via Science cloud website
 - Simply click on the instance and in the *console* you will see the desktop environment window
### 5.2. via remote desktop 
 - In the VM linux console: `sudo apt install xrdp`
 - In the **science cloud dashboard**: go to *Access & security* and then to create a new group and *Manage rules* there you can create a custom TCP rule with the port 3389. Direction = ingress. Create the rule and delete other rules in that group
 - In the **science cloud dashboard**: go to your instance and *edit security groups* . Add the newly created group together wtih the default group into the VM groups

## Attach a NAS
- `sudo apt install cifs-utils`
- If not created yet create the directory `sudo mkdir /mnt/smbdir`
- Mont the NAS: `sudo mount -t cifs -o rw,user=<uzh_username>,uid=<instance_username> //<nas_address> /mnt/smbdir`

#  Working in the Linux Virtual Machine
## Desktop environment limitations
Keep in mind the current desktop environment:
- is **NOT** capable to render advanced plots
- is laggy
- the *user* created does not have *sudo* permissions

Command line from your local terminal `ssh ubuntu@<ip of your VM>` will be better for things like:

- Mount NAS storage
- Copy files to directories accessible to all possible users
- Installations and upgrades of the VM (as they are not linked to a user)

## Suggested workflow 
- Use a **central storage location** that will be accessible from both local and cloud VM
- Ensure you or your team have a **snapshot** of a VM with the main programs you need
- When possible **test your pipeline locally** in your machine (e.g., with a couple of subjects)
- You may download and install toolboxes (e.g., EEGlab) locally and then copy them to the cloud or, if possible (not all will work), have them from the start in the *central storage*
- Use **relative paths** in your scripts (e.g., use a function to obtain the current directory and set it as your 'base directory') and **avoid platform-specific delimiters**. Matlab example: `fullfile(myBaseDirectory,'Data','Raw')` and NOT `~~[myBaseDirectory,'\Data\Raw']~~`
 
 
