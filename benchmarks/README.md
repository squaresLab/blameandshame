Instructions
============

Profiling
---------

To obtain detailed profiling information using one of the benchmarks within
this directory, simply execute the shell command below:

```
python3.6 -m cProfile -o profile.txt -s cumulative benchmark_annotate.py
```

where `benchmark_annotate.py` should be replaced with the script for a given
benchmark. `profile.txt` should be replaced with the name of the file to which
the profiling information should be written.
