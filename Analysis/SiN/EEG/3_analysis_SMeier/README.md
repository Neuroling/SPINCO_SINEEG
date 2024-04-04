# Naming conventions:

Scripts with suffixes
- ***_constants.py**  contains variable definitions that are constant through different scripts. Check this to see input and output parameters, paths, etc
- ***_functions.py** scripts contain functions called by runner scripts
- ***_runner.py** are the ones to run for performing the analyses
- **sketch_*_writing.py** are scripts to try out code and debug. They are disorganised ("spaghetti code")

Scripts specific to this folder:
- **SibMei_PreStim_Frequency_writing.py** is a script for S. Meier to adapt and experiment
    - Her adapted script is **SibMei_PreStim_Frequency_writing_25_03_2024.py**
- **PreStim_logitRegression.R** is an unused R-script that has a working multilevel logit regression. It is unused because we do all analyses in python.
- **defunct_PreStim_functions.py** is a collection of functions that used to be in **PreStim_functions.py** but are no longer used. They have been copy-pasted here in case of future recycling. Most are documented and working (in the context of the PreStimManager class, which they depend on)

# Notes on the Fitting Method

`LinAlgError: Singular matrix` sometimes occurs in the function `run_LogitRegression_withinSubj()` on the line `mdf = md.fit()`
- Documentation on `md.fit()` [here](https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.Logit.fit.html)
- The error is due to the fitting method for `md.fit()` - changing it from the default (`newton`) to any other method will circumvent the issue
- The error does not always occur at the same iteration/channel/timepoint
- However, it consistently occurs in the same subjects in one or both conditions (NV/SSN)
- The error is not due to some NaN in the data, because `np.isnan(np.min(data_array))` returns `False`
- This issue is described on github as issue [#5](https://github.com/Neuroling/SPINCO_SINEEG/issues/5#issue-2213560520)


## List of Options
The following methods exist:
- `newton` for Newton-Raphson, `nm` for Nelder-Mead
- `bfgs` for Broyden-Fletcher-Goldfarb-Shanno (BFGS)
- `lbfgs` for limited-memory BFGS with optional box constraints
- `powell` for modified Powell's method
- `cg` for conjugate gradient
- `ncg` for Newton-conjugate gradient
- `basinhopping` for global basin-hopping solver
- `minimize` for generic wrapper of scipy minimize (BFGS by default)
This list is copied from the [documentation](https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.Logit.fit.html)

## Conversion
`newton` and `nm` do not converge. All others do. 

## Fittig Time
```
%timeit mdf = md.fit() # default solver 'newton'
5.66 ms ± 66.2 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%timeit mdf = md.fit(method = "bfgs")
6.63 ms ± 25.9 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%timeit mdf = md.fit(method = "lbfgs")
2.35 ms ± 43.2 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```
There are significant differences in how fast the methods are. Considering the original plan was to run a regression for every subject, NoiseType, timepoint, channel, freqband, and iterate each 100 times, yielding a total of 23'654'400 regressions, a difference of half a second per regression becomes important.

