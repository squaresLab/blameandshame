#!/usr/bin/env python3
import unittest
from blameandshame.approach import Approach


class ApproachTestCase(unittest.TestCase):
    def test_localize(self):
        approach = Approach()
        self.assertRaises(NotImplementedError,
                          lambda: approach.localize(None, None, None, []))


if __name__ == '__main__':
    unittest.main()
