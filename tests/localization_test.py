#!/usr/bin/env python3
import os
import unittest
import pycodestyle
from blameandshame.components import Component, Line_C, Function_C, File_C
from blameandshame.localization import Line_Localization, File_Localization, Function_Localization, Localization

class LineLocalizationTestCase(unittest.TestCase):

    def check_one(data_map, expected):
        loc = Line_Localization()
        loc_result = loc.map_to_loc(data_map)         
        self.assertEqual(loc_result, expected)
        
    data_map = {}
    scope = [File_C("File1.java"), File_C("File2.java")]
    mapping = {Line_C("File1.java", 3): 0.3,
               Line_C("File1.java", 5): 0.5,
               Line_C("File2.java", 3): 0.8}
    expected = Line_Localization(mapping, scope)
    check_one(mapping, expected)


if __name__ == '__main__':
    unittest.main()
