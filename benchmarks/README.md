Instructions
============

We provide a simple command-line utility for benchmarking. A list of available
benchmarks can be obtained via the `list` command, as shown below.

```
$ python benchmark list
* annotate_closure
* last_commit_to_line
```

The `run` command can be used to execute a given benchmark, as shown below.
Optionally, the `--repeats` (or `-n`) option can be used to repeat the
benchmark a given number of times and to report timing statistics across those
runs.

```
$ python benchmark run last_commit_to_line
Running benchmark: last_commit_to_line

  num. executions: 1 executions
  mean time: 0.46 seconds
  std. dev: 0.00 seconds
  median time: 0.46 seconds

$ python benchmark run last_commit_to_line --repeats 30
Running benchmark: last_commit_to_line

  num. executions: 30 executions
  mean time: 0.47 seconds
  std. dev: 0.04 seconds
  median time: 0.46 seconds

```

Profiling
---------

To obtain detailed profiling information using one of the benchmarks within
this directory, simply execute the shell command below:

```
python -m cProfile -s cumulative benchmark run last_commit_to_line --repeats 30
```

where `benchmark_annotate.py` should be replaced with the script for a given
benchmark. `profile.txt` should be replaced with the name of the file to which
the profiling information should be written.
