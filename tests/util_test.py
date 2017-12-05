#!/usr/bin/env python3
import unittest
from blameandshame.base import  Project, Change
from blameandshame.util import  lines_modified_by_commit


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




if __name__ == '__main__':
    unittest.main()
