#!/usr/bin/env python3
import os
import unittest
from blameandshame.util import  repo_path, \
                                files_modified_by_commit, \
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


    def test_files_modified_by_commit(self):
        repo = get_repo('https://github.com/google/protobuf')
        files = files_modified_by_commit(repo, 'baed06e')
        self.assertEqual(files, frozenset(['objectivec/GPBCodedOutputStream.m']))




if __name__ == '__main__':
    unittest.main()
