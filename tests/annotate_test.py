#!/usr/bin/env python3
import unittest
from blameandshame.base import Project
from blameandshame.annotate import  annotate, \
                                    column_last_commit, \
                                    column_num_commits_to_file_since_commit


class AnnotateTestCase(unittest.TestCase):
    def test_annotate(self):
        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        actual = \
            annotate(project, project.repo.commit("e1d2532"), "file-one.txt")
        expected = [
            (1, 'Hello world.'),
            (2, ''),
            (3, 'How are you? :-)'),
            (4, ''),
            (5, 'Debugging time!')
        ]
        self.assertEqual(actual, expected)

        columns = [column_last_commit]
        actual = \
            annotate(project,
                     project.repo.commit("e1d2532"),
                     "file-one.txt",
                     columns)
        expected = [
            (1, 'Hello world.',     'e1d2532'),
            (2, '',                 '922e13d'),
            (3, 'How are you? :-)', '922e13d'),
            (4, '',                 '0d841d1'),
            (5, 'Debugging time!',  '0d841d1')
        ]
        self.assertEqual(actual, expected)


    def test_column_last_commit(self):
        def check_one(project, commit, filename, line, expected):
            commit = project.repo.commit(commit)
            last_commit = column_last_commit(project, commit, filename, line)
            self.assertEqual(last_commit, expected)

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'e1d2532', 'file-one.txt', 1, 'e1d2532')


    def test_column_num_commits_to_file_since_commit(self):
        def check_one(project, commit, filename, line, expected):
            commit = project.repo.commit(commit)
            num_commits = column_num_commits_to_file_since_commit(project,
                                                                  commit,
                                                                  filename,
                                                                  line)
            self.assertEqual(num_commits, expected)

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'e1d2532', 'file-one.txt', 1, 0)
