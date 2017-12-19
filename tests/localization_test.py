#!/usr/bin/env python3
import tempfile
import textwrap
import unittest
from blameandshame.localization import Localization


class LocalizationTestCase(unittest.TestCase):

    def test_from_file(self):
        """
        Tests the from_file function by creating a YAML file from a string
        and using from_file to import it.
        """
        simple_localization = textwrap.dedent(
            """
            !!python/object:blameandshame.localization.Localization
            _Localization__granularity: Simple
            _Localization__version: '0.0'
            mapping: {}
            scope: []
            """
        )
        f = tempfile.NamedTemporaryFile()
        f.write(simple_localization.encode())
        f.seek(0)
        l = Localization.from_file(f.name)
        self.assertEqual(l.granularity, "Simple")
        self.assertEqual(l.version, "0.0")
        self.assertEqual(l.mapping, {})
        self.assertEqual(l.scope, [])
        f.close()

if __name__ == '__main__':
    unittest.main()
