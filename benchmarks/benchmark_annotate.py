#!/usr/bin/env python3
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
__BENCHMARKS: Dict[str, Callable[[], None]] = {}


def benchmark(f: Callable[[], None]) -> Callable[[int], None]:
    def run(repeats : int = 1):
        print("Running benchmark: {}".format(f.__name__))
        t = Timer(f)
        print(t.timeit(number=repeats))
    return run


@benchmark
def annotate_closure() -> None:
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
    parser.add_argument('')



if __name__ == '__main__':
    annotate_closure()
