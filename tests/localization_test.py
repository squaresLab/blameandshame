#!/usr/bin/env python3
import tempfile
import textwrap
from typing import Dict, List, Type
import unittest
from blameandshame.localization import Localization
from blameandshame.components import Component, File_C, Function_C, Line_C


class LocalizationTestCase(unittest.TestCase):

    def test_from_file(self):
        """
        Tests the from_file function by creating a YAML file from a string
        and using from_file to import it.
        """
        def check_one(yaml_string: str,
                      granularity: Type[Component],
                      version: str,
                      mapping: Dict,
                      scope: List[Component]) -> None:
            f = tempfile.NamedTemporaryFile()
            f.write(yaml_string.encode())
            f.seek(0)
            l = Localization.from_file(f.name)
            f.close()
            self.assertEqual(l.granularity, granularity)
            self.assertEqual(l.version, version)
            self.assertEqual(l.mapping, mapping)
            self.assertEqual(l.scope, scope)

        simple_localization = textwrap.dedent(
            """
            !!python/object:blameandshame.localization.Localization
            _Localization__granularity: !!python/name:blameandshame.components.File_C
            _Localization__version: '0.0'
            mapping: {}
            scope: []
            """
        )
        check_one(simple_localization, File_C, "0.0", {}, [])
        simple_localization = textwrap.dedent(
            """
            !!python/object:blameandshame.localization.Localization
            _Localization__granularity: !!python/name:blameandshame.components.Function_C
            _Localization__version: '0.0'
            mapping: {}
            scope: []
            """
        )
        check_one(simple_localization, Function_C, "0.0", {}, [])
        simple_localization = textwrap.dedent(
            """
            !!python/object:blameandshame.localization.Localization
            _Localization__granularity: !!python/name:blameandshame.components.Line_C
            _Localization__version: '0.0'
            mapping: {}
            scope: []
            """
        )
        check_one(simple_localization, Line_C, "0.0", {}, [])


if __name__ == '__main__':
    unittest.main()
