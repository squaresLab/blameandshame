#!/usr/bin/env python3
import unittest
import pycodestyle


class StyleTestCase(unittest.TestCase):
    def test_conformance(self):
        style = pycodestyle.StyleGuide()
        result = style.check_files(['../src/blameandshame'])
        self.assertEqual(result.total_errors,
                         0,
                         "Found code style errors and/or warnings.")


if __name__ == '__main__':
    unittest.main()
