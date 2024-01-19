Current Issues (as of 18.01.2024):

If `n_jobs = -1` (in the constants), there's a big risk of the kernel getting 
killed mid-execution of the runner-script due to running out of RAM. 
Try one or more of the following:
  -  `n_jobs = None` (sequential processing, will take longer)
  -  running the amplitude extraction separate of the TFR feature extraction
  -  manually do it for every subject instead of looping (and opening a new console between subjects)