#!/usr/bin/env python3
import os
import unittest
from blameandshame.util import Change
from blameandshame.util import repo_path, \
                               files_in_commit, \
                               lines_in_commit, \
                               get_repo


class UtilTestCase(unittest.TestCase):
    def test_repo_path(self):
        cwd = os.getcwd()
        repos_dir = os.path.join(cwd, '.repos')

        self.assertEqual(repo_path('https://github.com/uber/pyro'),
                         os.path.join(repos_dir, 'pyro'))
        self.assertEqual(repo_path('https://github.com/google/protobuf'),
                         os.path.join(repos_dir, 'protobuf'))
        self.assertEqual(repo_path('https://github.com/cilium/cilium'),
                         os.path.join(repos_dir, 'cilium'))
        self.assertEqual(repo_path('https://github.com/golang/dep'),
                         os.path.join(repos_dir, 'dep'))
        self.assertEqual(repo_path('https://github.com/opencv/opencv.git'),
                         os.path.join(repos_dir, 'opencv'))


    def test_files_in_commit(self):
        repo = get_repo('https://github.com/google/protobuf')
        self.assertEqual(files_in_commit(repo, 'baed06e'),
                         frozenset(['objectivec/GPBCodedOutputStream.m']))
        self.assertEqual(files_in_commit(repo, '949596e'),
                         frozenset(['objectivec/GPBMessage.m']))
        self.assertEqual(files_in_commit(repo, 'cd5f49d', {Change.MODIFIED}),
                         frozenset(['ruby/travis-test.sh',
                                    'ruby/ext/google/protobuf_c/protobuf.c',
                                    'ruby/ext/google/protobuf_c/defs.c',
                                    'ruby/Rakefile',
                                    'Makefile.am',
                                    '.gitignore',
                                    'ruby/ext/google/protobuf_c/protobuf.h']))
        self.assertEqual(files_in_commit(repo, 'cd5f49d', {Change.ADDED}),
                         frozenset(['ruby/tests/gc_test.rb']))
        self.assertEqual(files_in_commit(repo, 'cd5f49d'),
                         frozenset(['ruby/travis-test.sh',
                                    'ruby/ext/google/protobuf_c/protobuf.c',
                                    'ruby/ext/google/protobuf_c/defs.c',
                                    'ruby/Rakefile',
                                    'Makefile.am',
                                    '.gitignore',
                                    'ruby/ext/google/protobuf_c/protobuf.h',
                                    'ruby/tests/gc_test.rb']))


    def test_lines_in_commit(self):
        repo = get_repo('https://github.com/google/protobuf')
        self.assertEqual(
            lines_in_commit(repo, 'baed06e'),
            (frozenset({('objectivec/GPBCodedOutputStream.m', 177)}),
             frozenset({('objectivec/GPBCodedOutputStream.m', 180)}))
        )
        # Only add
        self.assertEqual(
            lines_in_commit(repo, 'ac5371d'),
            (frozenset(), frozenset({('BUILD', 27), ('BUILD', 28)}))
        )
        # Only delete
        self.assertEqual(
            lines_in_commit(repo, 'd680159'),
            (frozenset({('src/google/protobuf/stubs/time.cc', 24)}),
             frozenset())
        )


if __name__ == '__main__':
    unittest.main()
