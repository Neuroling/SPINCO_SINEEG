## QUERIES 
- Exiting VM when in console (browser back botton? )
- Windows "remote desktop" window size.
  

## Access a WINDOWS VM from remote desktop
See documentation: https://docs.s3it.uzh.ch/how-to_articles/how_to_access_windows_vm_using_remote_desktop/

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

 ssh key generation

- Graphic user interface

https://docs.s3it.uzh.ch/how-to_articles/how_to_set_up_a_linux_terminal_environment_on_windows_10_with_windows_subsystem_for_linux/

