# Github

Github allows us version control of our script, backing up and sharing our code. More complex uses allow several people to work on some code (branching). 
Recommended to use **Github Desktop** is a GUI to manage pulls and push... This can facilitate these actions, otherwise they can be made from command line

The basic workflow for us would be:
- We clone a repository from **ORIGIN** (github web: e.g. ,.github.com/yourusername/reponame) to our local machine
- Work on our local folder edit scripts, add files etc. Then **COMMIT** (this will detect differences from your local folder to your origin). Then **PUSH** the changes to your origin (this will upload the changes in your online repo). In the website you will be able to see history of changes. 
- If you make changes in the origin directly (you are in the web and add some files or edit scripts). Then you can **PULL** origin, which will bring the stuff into your local 

NOTE: if you *FORK* someones repository you will make a copy of it in your machine or github repo. That copy will be independent: you will have full control over it and will be 'disconnected' from the original. If you *CLONE* a repository, you will copy it but changes on it will also go to the origin (e.g., Somebody Clones my repository, makes changes and then PUSH them to Github. I will then get some notification requesting to merge those changes with my version). So unless you are collaborating on some code it will be safer to just FORK and work on it independently. 

NOTE2: If you have data folders within your script folder you can add a file named ".gitignore" ( https://git-scm.com/docs/gitignore) specifying those folders containing data. This way when you PUSH to origin Github won't try to upload those files (else it will crash if you try to push too many files or too large). However, it may still be advisable to just have scripts in a separate folder and push the entire folder to Github (more clear workflow)...




![image](https://user-images.githubusercontent.com/13642762/198587002-af60c7a4-30b4-4976-a3b1-876e303b7295.png)

![image](https://user-images.githubusercontent.com/13642762/198583754-c46e6bfa-e98a-4d59-a94d-f2d2fa1deb0a.png)



