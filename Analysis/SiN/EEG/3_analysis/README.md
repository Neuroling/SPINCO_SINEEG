MVPA is done in MNE python toolbox. 
We first need to read the epoched EEGlab dataset and add some informatin to the trial events to encode all conditions of interest ('relabelling' )

TODO
[ ] subfolders and what they do
[ ] write primer on class objects


# ANALYSIS SCRIPTS
author: samuelmull

## Script naming conventions

In each folder you will find scripts with the following naming conventions:  
- **\*_runner.py** is the main script for finished code   
- **\*_functions.py** is a collection of functions that are called by the \*_runner.py script  
- **\*_constants.py** contains variables that do not change across files, such as subject IDs    
- **sketch_\*_writing.py** is for trying out and debugging code before putting it in \*_functions.py   

The runner scripts are designed to be as minimalistic as possible. All the nitty-gritty is hidden in the function scripts.   

Many functions have adjustable parameters. Never be afraid to type `help(SomeManager.someFunction)` to see the docstring for that function.

## A short primer on python classes and class objects

Each function script contains a class. A class is a neat way to collect functions and accumulate data across those functions. The class, for instance `MVPAManager` from the *MVPA_functions.py* script, is initialised in the runner script, like so:  

```
import MVPA_functions as functions

MVPAManagerObj = functions.MVPAManager()
```

Now, we have the class object `MVPAManagerObj`, which, as it has been initialised (see the `__init__` function in MVPA_functions.py), already has started an empty dictionary to store metadata in with every function called.  

We can now call functions from the `MVPAManager` class by running `MVPAManagerObj.someFunction()`.
