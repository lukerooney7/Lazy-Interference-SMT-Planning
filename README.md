# Lazy Interference Evaluation in Planning as SMT
## Installing pyPMT

Install the package using `pip`:
```
python -m pip install .
```

## Running Lazy Evaluation in pyPMT

Navigate to pyPMT folder:
```
cd pypmt
```
To run pyPMT on a problem from the CLI, type:
```
 python3 pypmtcli.py 'solve', '-d', 'path_to_domain.pddl', '-p', 'path_to_problem.pddl', '-e', 'encoding_name' '-v' '4'
```
encoding_name represents the configuration key, which can be any of the following:

| ∀-step plans     | ∃-step plans     | Description                                                             |
|------------------|------------------|-------------------------------------------------------------------------|
| forall           | exists           | Eager implementation (invokes Python propagator)                        |
| forall-lazy      | exists-lazy      | Naive Lazy implementation                                               |
| forall-final     | exists-final     | Generate & Test lazy implementation                                     |
| forall-code      | exists-code      | Code-optimised lazy implementation                                      |
| forall-prop      | exists-prop      | Neighbours & Ghost Node propagation optimisation in lazy implementation |
| forall-stepshare | exists-stepshare | Step-share propagation optimisation in lazy implementation              |
| forall-decide    | exists-decide    | Overriding Decides() callback optimisation implementation               |
| forall-noprop    | exists-noprop    | Eager implementation in C++                                             |
| forall-frame     | exists-frame     | Attempt at lazy frame evaluation (NOT FINISHED!)                        |

All domains and instances can be found in /domains folder, which are split into classical and numeric. For example, 
run the above command with:
```
 -d = domains/classical/rovers/domain.pddl
 -p = domains/classical/rovers/p01.pddl
```
All instances in the domain folder were tested and evaluated in the dissertation report, however if running single
instances on a PC, only attempt to run lower umber ones as they take a long time to solve. Some suggested examples,
which are quick to validate correctness are:
* Classical - airport/rovers/tpp
* Numeric - counters/mprime/zenotravel

## Code Explanation
All code for propagators is stored in pypmt/propagators

Changes made to other pyPMT files:
* encoders/basic.py
* modifiers/parallel modifier.py
* config.py
* planner/SMTActionPropagator.py

The data collected displayed in this dissertation is stored in the following files:
* all.csv (Planning  for all solved domain instances for all planners)
* pypmt/stats.csv (Solve statistics for a sample set of instances including mutexes added, propagations, conflicts etc.)

All visualisation code is in the /analysis folder:
* visualisation.py
* solveStatsVisualisations.py
* stepCount.py
* fileToCSV.py

Code that was not used in the report, but just to visualise to help debugging, and explore graph properties is in the 
/analysis/graph-analysis folder

