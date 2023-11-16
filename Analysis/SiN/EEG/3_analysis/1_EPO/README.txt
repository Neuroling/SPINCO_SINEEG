EPO folder is for all scripts and files handling epoching data

EPO_runner.py is the main script for finished code
EPO_helper.py is a collection of functions for handling epoching
EPO_constants.py contains variables that do not change across files, such as subject IDs
EPO_writing.py is for trying out and debugging code before putting it in EPO_helper.py


-----Event Labels-----

NoiseType / StimulusType / DegradationLevel / Accuracy / Voice
    
    X____ NoiseType: NV = 1, SSN = 2
    _X___ Stimulus Type: Call = 1, Colour = 2, Number = 3
    __X__ Degradation Level: Lv1 = 1, Lv2 = 2, Lv3 = 3
    ___X_ Accuracy: Incorrect = 0, Correct = 1
    ____X Voice: Feminine (Neural2-F) = 1, Masculine (Neural2-D) = 2
  
  
This allows you to filter the epochs using the event labels, i.e. by:
    epochs.__getitem__('NV') --------> will return all epochs with NV
    epochs.__getitem__('Lv1/call') --> will return all epochs with Lv1 degradation and CallSign