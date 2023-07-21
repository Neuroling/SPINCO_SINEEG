# QUERIES  ! 
- Linux graphic interface
- can I make a Linux VM accessible from internet browser in any computer? 
- Windows matlab licensing
- Windows as remote desktop. Recommended to create user profiles? Does this persists after closing the VM ?(in the snapshot) 
- Transfer a VM (snapshot ) from one project to another 
 
# Linux VM with Graphical interface 
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
- Mont instance: `sudo mount -t cifs -o rw,user=<uzh_username>,uid=<instance_username> //<nas_address> /mnt/smbdir`
















# -----------------------------------


# Access a Linux VM from Windows
## Set up ssh key
See the 'Getting access to my VM' of the training material
https://docs.s3it.uzh.ch/cloud/training/training_handout/

It is likely you need to install Openssh feature for Windows(https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse?tabs=powershell#install-openssh-for-windows)
I had to install it copying the commands for powershell (up to the section connect to Open SSH server, excluding that) 

Once done go to power shell. In short: 
Go to windows `*powershell*`
- You will `ssh-keygen -t rsa -b 4096` to generate a key. Go with the defaults and it will save some files in your home directory .ssh
- From those files you will need to copy the public Key in the VM instance. So type  `cat ~/.ssh/id_rsa.pub` and copy the entire output. Go to the *Cloud dashboard* and paste it into the import KEY options of *Access and security*
- Then do `ssh -i ~/.ssh/id_rsa ubuntu@<your-instance-ip-address>` to access it. Get the IP from the cloud dashboard
- Next time you can just do `ssh ubuntu@<your-instance-ip-address>`
Now you are in: 
 
 ![image](https://github.com/Neuroling/SPINCO_SINEEG/assets/13642762/e3b59f2d-ac87-4f6d-a85c-a6a1bd7b073e)

 


## Attaching NAS
https://docs.s3it.uzh.ch/cloud/faq/#how-do-i-connect-to-an-smb-network-attached-storage-device-nas-from-a-sciencecloud-instance




--------------------------------------------
## Having Linux in Windows
Documentation: 
https://docs.s3it.uzh.ch/how-to_articles/how_to_set_up_a_linux_terminal_environment_on_windows_10_with_windows_subsystem_for_linux/

### Enable WSL (windows subsystem for Linux)
In windows powershell (with admin permits) type: `Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux`

### Download Ubuntu for WSL from Microsoft store
Go to https://www.microsoft.com/en-us/p/ubuntu/9nblggh4msv6 

### Set up ubuntu
#### User and password
If you start as a root after installation you need to create a user and password
- `sudo adduser <username>`
- It will prompt you to enter a password (twice)
- You can add other info like full name etc or skip with ENTER
Login as the new user
- `login <username>`

#### ssh key generation
Once logged in as user (in your local Ubuntu console):
- Type this: `ssh-keygen -t rsa -b 4096`
- You can press enter when asked about the files in which to save it, to choose default
- It will ask to enter a passphrase or leave this empty
- Now you can access `cat ~./.ssh/id_rsa.pub` to see the public key that should have been generated

### Graphic user interface
https://docs.s3it.uzh.ch/how-to_articles/how_to_set_up_a_linux_terminal_environment_on_windows_10_with_windows_subsystem_for_linux/





  

## Access a WINDOWS VM from remote desktop
See documentation: https://docs.s3it.uzh.ch/how-to_articles/how_to_access_windows_vm_using_remote_desktop/
# Windows setup 
At the beginning (after creating the VM) we start as Admin 

# Windows display settings

- Monitor . Right click in desktop, display settings and then advanced display settings. Change resolution to find the right size
- Mouse. Turn black. Right click in desktop then personalize / themes/ mouse pointer settings

