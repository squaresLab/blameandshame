#!/usr/bin/env python3
import os
import unittest
from blameandshame.base import Project, Change
from datetime import timedelta

class ProjectTestCase(unittest.TestCase):
    def test_url_to_path(self):
        repos_dir = os.path.join(os.getcwd(), '.repos')

        self.assertEqual(Project._url_to_path('https://github.com/uber/pyro'),
                         os.path.join(repos_dir, 'pyro'))
        self.assertEqual(Project._url_to_path('https://github.com/google/protobuf'),
                         os.path.join(repos_dir, 'protobuf'))
        self.assertEqual(Project._url_to_path('https://github.com/cilium/cilium'),
                         os.path.join(repos_dir, 'cilium'))
        self.assertEqual(Project._url_to_path('https://github.com/golang/dep'),
                         os.path.join(repos_dir, 'dep'))
        self.assertEqual(Project._url_to_path('https://github.com/opencv/opencv.git'),
                         os.path.join(repos_dir, 'opencv'))


    def test_files_in_commit(self):
        project = Project.from_url('https://github.com/google/protobuf')
        self.assertEqual(project.files_in_commit(project.repo.commit('baed06e')),
                         frozenset(['objectivec/GPBCodedOutputStream.m']))
        self.assertEqual(project.files_in_commit(project.repo.commit('949596e')),
                         frozenset(['objectivec/GPBMessage.m']))
        self.assertEqual(project.files_in_commit(project.repo.commit('cd5f49d'), {Change.MODIFIED}),
                         frozenset(['ruby/travis-test.sh',
                                    'ruby/ext/google/protobuf_c/protobuf.c',
                                    'ruby/ext/google/protobuf_c/defs.c',
                                    'ruby/Rakefile',
                                    'Makefile.am',
                                    '.gitignore',
                                    'ruby/ext/google/protobuf_c/protobuf.h']))
        self.assertEqual(project.files_in_commit(project.repo.commit('cd5f49d'), {Change.ADDED}),
                         frozenset(['ruby/tests/gc_test.rb']))
        self.assertEqual(project.files_in_commit(project.repo.commit('cd5f49d')),
                         frozenset(['ruby/travis-test.sh',
                                    'ruby/ext/google/protobuf_c/protobuf.c',
                                    'ruby/ext/google/protobuf_c/defs.c',
                                    'ruby/Rakefile',
                                    'Makefile.am',
                                    '.gitignore',
                                    'ruby/ext/google/protobuf_c/protobuf.h',
                                    'ruby/tests/gc_test.rb']))


    def test_commits_to_repo(self):
        def check_one(project, expected, after = None, before = None):
            expected = [project.repo.commit(sha) for sha in expected]
            after_commit = project.repo.commit(after) if after else None
            before_commit = project.repo.commit(before) if before else None
            self.assertEqual(
                project.commits_to_repo(after = after_commit,
                                        before = before_commit),
                expected
            )

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, ['e1d2532', '71622b3', '9ca70f7'],
                  after = '2282c66', before = 'e1d2532')

        # Starting from first commit
        check_one(project, ['922e13d', '422cab3'],
                  after = '964adc5', before = '922e13d')

        # after == before
        check_one(project, [],
                  after = '2282c66', before = '2282c66')

        # no before
        check_one(project, ['422cab3', '964adc5'],
                  before = '422cab3')

    def test_commits_to_file(self):
        def check_one(project, filename, expected, after = None, before = None):
            expected = [project.repo.commit(sha) for sha in expected]
            after_commit = project.repo.commit(after) if after else None
            before_commit = project.repo.commit(before) if before else None
            self.assertEqual(
                project.commits_to_file(filename,
                                        after = after_commit,
                                        before = before_commit),
                expected
            )

        project = Project.from_url('https://github.com/php/php-src')
        check_one(project, 'ext/ext_skel.php',
                  ['216d711', 'f35f459', 'b079cc2', '941dc72'],
                  before = '216d711')

        project = Project.from_url('https://github.com/google/protobuf')
        check_one(project, 'php/composer.json',
                  ['21b0e55', 'b9b34e9', '6b27c1f', '46ae90d'],
                  before = '21b0e55')

        # corner case: file is renamed once
        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'file-one.txt',
                  ['474ea04', '922e13d', '422cab3'],
                  before = '474ea04')

        # After first commit
        check_one(project, 'file-one.txt', ['474ea04', '922e13d', '422cab3'],
                  after = '964adc5', before = '474ea04')


    def test_commits_to_line(self):
        def check_one(project, filename, lineno, expected):
            expected = [project.repo.commit(sha) for sha in expected]
            self.assertEqual(project.commits_to_line(filename, lineno, before=expected[0]),
                             expected)

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'file.txt', 1, ['922e13d', '422cab3'])


    def test_authors_of_file(self):
        def check_one(project, filename, before, expected):
            before = project.repo.commit(before)
            actors = project.authors_of_file(filename, before=before)
            authors = frozenset(a.name for a in actors)
            self.assertEqual(authors, frozenset(expected))

        project = Project.from_url('https://github.com/google/protobuf')
        check_one(project, 'php/composer.json', '21b0e55',
                  ['Paul Yang', 'michaelbausor', 'Brent Shaffer'])
        check_one(project, 'php/composer.json', '6b27c1f',
                  ['Paul Yang'])


    def test_last_commit_to_line(self):
        def check_one(project, filename, line, before, expected):
            before = project.repo.commit(before)
            if expected is not None:
                expected = project.repo.commit(expected)
            actual = project.last_commit_to_line(filename, line, before)
            self.assertEqual(actual, expected)

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'file-one.txt', 1, '9ca70f7', '922e13d')
        check_one(project, 'file-one.txt', 5, 'e1d2532', '0d841d1')
        check_one(project, 'file-one.txt', 1, '422cab3', None)
        check_one(project, 'file-one.txt', 1, 'e1d2532', 'e1d2532')


    def test_lines_modified_by_commit(self):
        project = Project.from_url('https://github.com/google/protobuf')
        self.assertEqual(
            project.lines_modified_by_commit(project.repo.commit('baed06e')),
            (frozenset({('objectivec/GPBCodedOutputStream.m', 177)}),
             frozenset({('objectivec/GPBCodedOutputStream.m', 180)}))
        )
        # Only add
        self.assertEqual(
            project.lines_modified_by_commit(project.repo.commit('ac5371d')),
            (frozenset(), frozenset({('BUILD', 27), ('BUILD', 28)}))
        )
        # Only delete
        self.assertEqual(
            project.lines_modified_by_commit(project.repo.commit('d680159')),
            (frozenset({('src/google/protobuf/stubs/time.cc', 24)}),
             frozenset())
        )

    def test_authors_of_line(self):
        def check_one(project, filename, line, before, expected):
            before = project.repo.commit(before)
            actors = project.authors_of_line(filename, line, before=before)
            authors = frozenset(a.name for a in actors)
            self.assertEqual(authors, frozenset(expected))

        project = Project.from_url('https://github.com/google/protobuf')
        check_one(project, 'php/composer.json', 2, '21b0e55',
                  ['Paul Yang'])

    def test_time_between_commits(self):
        project = Project.from_url('https://github.com/google/protobuf')

        delta = Project.time_between_commits(project.repo.commit("ac5371d"),
                                             project.repo.commit("9935829"))
        self.assertEqual(delta, timedelta(seconds=10628))

        delta = Project.time_between_commits(project.repo.commit("9935829"),
                                             project.repo.commit("ac5371d"))
        self.assertEqual(delta, timedelta(seconds=10628))

    def test_num_lines_in_file(self):
        def check_one(project, filename, version, expected):
            version = project.repo.commit(version)
            actual = project._num_lines_in_file(filename, version)
            self.assertEqual(actual, expected)

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'file-one.txt', '86c9401', 7)
        check_one(project, 'file-one.txt', '0d841d1', 5)
        check_one(project, 'file-one.txt', '4d6c7f4', 3)
        check_one(project, 'file.txt', '422cab3', 1)

    def test_percentile_age_of_line(self):
        def check_one(project,filename,version,line,expected):
            commit = project.repo.commit(version)
            perc = project.percentile_age_of_line(commit, filename, line)
            rounded=round(perc,2)
            self.assertEqual(rounded, expected)

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project,"file-one.txt" ,"0d841d1", 3, 0.40)
        check_one(project,"file-one.txt" ,"0d841d1", 1, 0.40)
        check_one(project,"file-one.txt" ,"0d841d1", 5, 0)
        check_one(project,"file-one.txt" ,"86c9401", 1, 0.28999999999999998)
        check_one(project,"file-one.txt" ,"86c9401", 5, 0.42999999999999999)
        check_one(project,"file-one.txt" ,"86c9401", 6, 0)

    def test_relative_age_of_line(self):
        def check_one(project,filename,version,line,expected):
            commit = project.repo.commit(version)
            rage = project.relative_age_of_line(commit, filename, line)
            rounded=round(rage,2)
            self.assertEqual(rounded, expected)
            
        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project,"file-one.txt" ,"0d841d1", 3, 1)
        check_one(project,"file-one.txt" ,"0d841d1", 1, 1)
        check_one(project,"file-one.txt" ,"0d841d1", 5, 0)
        check_one(project,"file-one.txt" ,"86c9401", 7, 0)
        check_one(project,"file-one.txt" ,"86c9401", 2, 1)
        check_one(project,"file-one.txt" ,"86c9401", 5, 0.88)
        check_one(project,"file-one.txt" ,"86c9401", 1, 0.73)
        
if __name__ == '__main__':
    unittest.main()
