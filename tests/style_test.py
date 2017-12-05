#!/usr/bin/env python3
import os
import unittest
import pycodestyle


class StyleTestCase(unittest.TestCase):
    def test_conformance(self):
        style = pycodestyle.StyleGuide()
        test_dir = os.path.dirname(os.path.abspath(__file__))
        src_dir = os.path.join(test_dir, '../src/blameandshame')
        result = style.check_files([src_dir])
        self.assertEqual(result.total_errors,
                         0,
                         "Found code style errors and/or warnings.")


if __name__ == '__main__':
    unittest.main()
