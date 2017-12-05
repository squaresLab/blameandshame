#!/usr/bin/env python3
import unittest
from blameandshame.base import  Project, Change
from blameandshame.util import  lines_modified_by_commit, \
                                last_commit_to_line


class UtilTestCase(unittest.TestCase):
    def test_lines_modified_by_commit(self):
        project = Project.from_url('https://github.com/google/protobuf')
        repo = project.repo
        self.assertEqual(
            lines_modified_by_commit(repo, 'baed06e'),
            (frozenset({('objectivec/GPBCodedOutputStream.m', 177)}),
             frozenset({('objectivec/GPBCodedOutputStream.m', 180)}))
        )
        # Only add
        self.assertEqual(
            lines_modified_by_commit(repo, 'ac5371d'),
            (frozenset(), frozenset({('BUILD', 27), ('BUILD', 28)}))
        )
        # Only delete
        self.assertEqual(
            lines_modified_by_commit(repo, 'd680159'),
            (frozenset({('src/google/protobuf/stubs/time.cc', 24)}),
             frozenset())
        )


    def test_last_commit_to_line(self):
        project = Project.from_url('https://github.com/squaresLab/blameandshame-test-repo')
        repo = project.repo
        self.assertEqual(last_commit_to_line(repo, 'file-one.txt', 1,
                                             repo.commit('9ca70f7')),
                         repo.commit('922e13d'))
        self.assertEqual(last_commit_to_line(repo, 'file-one.txt', 5,
                                             repo.commit('e1d2532')),
                         repo.commit('0d841d1'))
        self.assertEqual(last_commit_to_line(repo, 'file-one.txt', 1,
                                             repo.commit('422cab3')),
                         None)
        self.assertEqual(last_commit_to_line(repo, 'file-one.txt', 1,
                                             repo.commit('e1d2532')),
                         repo.commit('e1d2532'))


if __name__ == '__main__':
    unittest.main()
