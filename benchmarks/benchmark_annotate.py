#!/usr/bin/env python3.6
from blameandshame.base import Project
from blameandshame.annotate import annotate, \
                                   column_last_commit, \
                                   column_num_file_commits_after_modified, \
                                   column_num_project_commits_after_modified, \
                                   column_num_days_since_modified

def benchmark_annotate_closure():
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


if __name__ == '__main__':
    benchmark_annotate_closure()
