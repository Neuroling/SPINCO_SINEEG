# Naming conventions:

Scripts with suffixes
- *_constants.py  contains variable definitions that are constant through different scripts. Check this to see input and output parameters, paths, etc
- *_functions.py scripts contain functions called by runner scripts
- *_runner.py are the ones to run for performing the analyses
- sketch_*_writing.py are scripts to try out code and debug. They are disorganised ("spaghetti code")

- `PreStim_logitRegression.R` is an unused R-script that has a working multilevel logit regression. It is unused because we do all analyses in python.


# Processed subjects:
        NV   SiSSN
s001   done
s002   done
s003   done
s004   done
s005   Err1
s006   done
s007   done
s008   done
s009   done
s010   Err1
s011   done
s012   Err1
s013   running...
s015   

Err1 refers to `LinAlgError: Singular matrix` which sometimes occurs in the function `run_LogitRegression_withinSubj()` on the line `mdf = md.fit()`
I (samuemu) took a screenshot of the most recent calls in the console.
I do not know why it occurs only in some subjects in some conditions, and also not during every iteration
It may be only on some timepoints or channels? Need to test further.
