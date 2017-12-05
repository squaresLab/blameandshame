#!/usr/bin/env python3
import os
import unittest
from blameandshame.base import Project
from blameandshame.annotate import  annotate, \
                                    column_last_commit


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
