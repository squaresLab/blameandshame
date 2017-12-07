#!/usr/bin/env python3
import numpy as np
from typing import Callable, Dict
from argparse import ArgumentParser
from timeit import Timer
from blameandshame.base import Project
from blameandshame.annotate import annotate, \
                                   column_last_commit, \
                                   column_num_file_commits_after_modified, \
                                   column_num_project_commits_after_modified, \
                                   column_num_days_since_modified


# Maintains a registry of named benchmarks
__BENCHMARKS__: Dict[str, Callable[[], None]] = {}


def benchmark(f: Callable[[], None]) -> Callable[[int], None]:
    """
    Registers a given function as a benchmark.
    """
    fn = f.__name__
    def run(repeats : int = 1):
        print("Running benchmark: {}".format(fn))
        t = Timer(f)
        times = t.repeat(number=1, repeat=repeats)
        print("  num. executions: {}".format(len(times)))
        print("  mean time: {%.2f} seconds".format(np.mean(times)))
        print("  std. dev: {%.2f}".format(np.std(times)))
        print("  median time: {%.2f} seconds\n".format(np.median(times)))
    __BENCHMARKS__[fn] = run
    return run


@benchmark
def last_commit_to_line() -> None:
    """
    Computes the last commit that was made to a given line in a historical
    version of the closure compiler.
    """
    project = Project.from_url('https://github.com/google/closure-compiler')
    fix_sha = '1dfad50'
    commit = project.repo.commit('{}~1'.format(fix_sha))
    filename = 'src/com/google/javascript/jscomp/RemoveUnusedVars.java'
    line = 372

    column_last_commit(project, commit, filename, line)


@benchmark
def annotate_closure() -> None:
    """
    Annotates the source code for a single file from a historical version
    of the closure compiler project with four additional columns.
    """
    project = Project.from_url('https://github.com/google/closure-compiler')
    fix_sha = '1dfad50'
    commit = project.repo.commit('{}~1'.format(fix_sha))
    filename = 'src/com/google/javascript/jscomp/RemoveUnusedVars.java'

    cols = [
        column_last_commit,
        column_num_file_commits_after_modified,
        column_num_project_commits_after_modified,
        column_num_days_since_modified
    ]

    annotate(project, commit, filename, cols)


def build_parser() -> ArgumentParser:
    parser = \
        ArgumentParser(description='Used to conduct performance benchmarks.')


    # discover all benchmarks
    benchmark_names = list(__BENCHMARKS__.keys())
    parser.add_argument('')


if __name__ == '__main__':
    last_commit_to_line(repeats=30)
