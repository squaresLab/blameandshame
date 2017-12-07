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

To obtain detailed profiling information using one of the benchmarks within
this directory, the `--profile` flag can be passed to `run`, as shown below.

```
$ python benchmark run last_commit_to_line --repeats 30 --profile

TODO
```
