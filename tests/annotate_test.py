#!/usr/bin/env python3
import unittest
from blameandshame.base import Project
from blameandshame.annotate import  annotate, \
                                    use_different_commit, \
                                    column_last_commit, \
                                    column_num_file_commits_after_modified, \
                                    column_num_project_commits_after_modified, \
                                    column_num_days_since_modified, \
                                    column_was_modified_by_commit, \
                                    column_project_name, \
                                    column_project_age_commits, \
                                    column_file_age_commits_to_project, \
                                    column_file_age_commits_to_file


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


    def test_use_different_commit(self):
        def check_one(fun, project, commit, different_commit, filename, line, expected):
            commit = project.repo.commit(commit)
            different_commit = project.repo.commit(different_commit)
            modified = use_different_commit(fun, different_commit)
            result = modified(project, commit, filename, line)
            self.assertEqual(result, expected)
        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(column_last_commit, project, '0d841d1', 'e1d2532', 'file-one.txt', 1, 'e1d2532')
        check_one(column_num_file_commits_after_modified, project, '0d841d1', 'e1d2532',
                  'file-one.txt', 2, '4')


    def test_column_last_commit(self):
        def check_one(project, commit, filename, line, expected):
            commit = project.repo.commit(commit)
            last_commit = column_last_commit(project, commit, filename, line)
            self.assertEqual(last_commit, expected)

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'e1d2532', 'file-one.txt', 1, 'e1d2532')


    def test_column_num_file_commits_after_modified(self):
        def check_one(project, commit, filename, line, expected):
            commit = project.repo.commit(commit)
            num_commits = column_num_file_commits_after_modified(project,
                                                                 commit,
                                                                 filename,
                                                                 line)
            self.assertEqual(num_commits, expected)

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'e1d2532', 'file-one.txt', 1, '0')
        check_one(project, 'e1d2532', 'file-one.txt', 2, '4')
        check_one(project, 'e1d2532', 'file-one.txt', 4, '2')


    def test_column_num_project_commits_after_modified(self):
        def check_one(project, commit, filename, line, expected):
            commit = project.repo.commit(commit)
            num_commits = column_num_project_commits_after_modified(project,
                                                                    commit,
                                                                    filename,
                                                                    line)
            self.assertEqual(num_commits, expected)

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'e1d2532', 'file-one.txt', 1, '0')
        check_one(project, 'e1d2532', 'file-one.txt', 2, '9')
        check_one(project, 'e1d2532', 'file-one.txt', 4, '6')


    def test_column_num_days_since_modified(self):
        def check_one(project, commit, filename, line, expected):
            commit = project.repo.commit(commit)
            num_days = column_num_days_since_modified(project,
                                                      commit,
                                                      filename,
                                                      line)
            self.assertEqual(num_days, expected)

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'e1d2532', 'file-one.txt', 1, '0')
        check_one(project, 'e1d2532', 'file-one.txt', 3, '1')

    def test_column_was_modified_by_commit(self):
        def check_one(project, commit, filename, line, expected):
            commit = project.repo.commit(commit)
            modified = column_was_modified_by_commit(project,
                                                     commit,
                                                     filename,
                                                     line)
            self.assertEqual(modified, expected)

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'e1d2532', 'file-one.txt', 1, 'true')
        check_one(project, 'e1d2532', 'file-one.txt', 3, 'false')

    def test_column_project_name(self):
        def check_one(project, expected):
            name = column_project_name(project, None, "", 1)
            self.assertEqual(name, expected)

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'blameandshame-test-repo')
        project = Project.from_url('https://github.com/google/protobuf')
        check_one(project, 'protobuf')

    def test_column_project_age_commits(self):
        def check_one(project, commit, expected):
            commit = project.repo.commit(commit)
            self.assertEqual(column_project_age_commits(project, commit, "", 0),
                             expected)
        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'a351329', '18')
        check_one(project, '71622b3', '11')

    def test_column_file_age_commits_to_project(self):
        def check_one(project, commit, filename, expected):
            commit = project.repo.commit(commit)
            self.assertEqual(column_file_age_commits_to_project(project, commit, filename, 0),
                             expected)
        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'a351329', 'testfile.c', '5')
        check_one(project, '71622b3', 'file-one.txt', '9')

    def test_column_file_age_commits_to_file(self):
        def check_one(project, commit, filename, expected):
            commit = project.repo.commit(commit)
            self.assertEqual(column_file_age_commits_to_file(project, commit, filename, 0),
                             expected)
        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'a351329', 'testfile.c', '5')
        check_one(project, '86c9401', 'file-one.txt', '7')
