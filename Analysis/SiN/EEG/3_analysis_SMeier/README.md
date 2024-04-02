# Naming conventions:

Scripts with suffixes
- *_constants.py  contains variable definitions that are constant through different scripts. Check this to see input and output parameters, paths, etc
- *_functions.py scripts contain functions called by runner scripts
- *_runner.py are the ones to run for performing the analyses
- sketch_*_writing.py are scripts to try out code and debug. They are disorganised ("spaghetti code")

- SibMei_PreStim_Frequency_writing.py is a script for S. Meier to adapt and experiment
- `PreStim_logitRegression.R` is an unused R-script that has a working multilevel logit regression. It is unused because we do all analyses in python.


# Notes

`LinAlgError: Singular matrix` sometimes occurs in the function `run_LogitRegression_withinSubj()` on the line `mdf = md.fit()`
- The error does not always occur at the same iteration/channel/timepoint
- However, it consistently occurs in the same subjects in one or both conditions (NV/SSN)
- The error is not due to some NaN in the data, because `np.isnan(np.min(data_array))` returns `False`

UPDATE:
- The error is due to the solver for `md.fit()` - changing it from the default (`newton`) to `bfgs` or to `lbfgs` will circumvent the issue
- Documentation on `md.fit()` https://www.statsmodels.org/stable/generated/statsmodels.discrete.discrete_model.Logit.fit.html

## Solvers and how fast they are:
```
%timeit mdf = md.fit() # default solver 'newton'
5.66 ms ± 66.2 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%timeit mdf = md.fit(method = "bfgs")
6.63 ms ± 25.9 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%timeit mdf = md.fit(method = "lbfgs")
2.35 ms ± 43.2 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```
So I'm going with the `lbfgs` solver as default for `run_LogitRegression_withinSubj()`
