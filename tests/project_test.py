#!/usr/bin/env python3
import os
import unittest
from blameandshame.base import Project, Change


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
        self.assertEqual(project.files_in_commit('baed06e'),
                         frozenset(['objectivec/GPBCodedOutputStream.m']))
        self.assertEqual(project.files_in_commit('949596e'),
                         frozenset(['objectivec/GPBMessage.m']))
        self.assertEqual(project.files_in_commit('cd5f49d', {Change.MODIFIED}),
                         frozenset(['ruby/travis-test.sh',
                                    'ruby/ext/google/protobuf_c/protobuf.c',
                                    'ruby/ext/google/protobuf_c/defs.c',
                                    'ruby/Rakefile',
                                    'Makefile.am',
                                    '.gitignore',
                                    'ruby/ext/google/protobuf_c/protobuf.h']))
        self.assertEqual(project.files_in_commit('cd5f49d', {Change.ADDED}),
                         frozenset(['ruby/tests/gc_test.rb']))
        self.assertEqual(project.files_in_commit('cd5f49d'),
                         frozenset(['ruby/travis-test.sh',
                                    'ruby/ext/google/protobuf_c/protobuf.c',
                                    'ruby/ext/google/protobuf_c/defs.c',
                                    'ruby/Rakefile',
                                    'Makefile.am',
                                    '.gitignore',
                                    'ruby/ext/google/protobuf_c/protobuf.h',
                                    'ruby/tests/gc_test.rb']))


    def test_commits_to_line(self):
        def check_one(project, filename, lineno, expected):
            expected = [project.repo.commit(sha) for sha in expected]
            self.assertEqual(project.commits_to_line(filename, lineno, until=expected[0]),
                             expected)

        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'file.txt', 1, ['922e13d', '422cab3'])


    def test_commits_to_file(self):
        def check_one(project, filename, expected):
            expected = [project.repo.commit(sha) for sha in expected]
            self.assertEqual(project.commits_to_file(filename, until=expected[0]),
                             expected)

        project = Project.from_url('https://github.com/php/php-src')
        check_one(project, 'ext/ext_skel.php', ['216d711', 'f35f459', 'b079cc2', '941dc72'])

        project = Project.from_url('https://github.com/google/protobuf')
        check_one(project, 'php/composer.json', ['21b0e55', 'b9b34e9', '6b27c1f', '46ae90d'])

        # corner case: file is renamed once
        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        check_one(project, 'file-one.txt', ['474ea04', '922e13d', '422cab3'])


if __name__ == '__main__':
    unittest.main()
