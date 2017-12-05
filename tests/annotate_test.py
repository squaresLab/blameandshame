#!/usr/bin/env python3
import os
import unittest
from blameandshame.base import Project
from blameandshame.annotate import annotate


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
