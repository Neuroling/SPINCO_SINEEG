## QUERIES  ! 
- Linux graphic interface
- can I make a Linux VM accessible from internet browser in any computer? 
- Windows matlab licensing
- Windows as remote desktop. Recommended to create user profiles? Does this persists after closing the VM ?(in the snapshot) 
- Transfer a VM (snapshot ) from one project to another 
 






  

## Access a WINDOWS VM from remote desktop
See documentation: https://docs.s3it.uzh.ch/how-to_articles/how_to_access_windows_vm_using_remote_desktop/
# Windows setup 
At the beginning (after creating the VM) we start as Admin 

# Windows display settings

- Monitor . Right click in desktop, display settings and then advanced display settings. Change resolution to find the right size
- Mouse. Turn black. Right click in desktop then personalize / themes/ mouse pointer settings









## Access a LINUX VM from remote desktop
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

