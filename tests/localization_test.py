#!/usr/bin/env python3
import os
import unittest
import pycodestyle
from blameandshame.components import Component, Line_C, Function_C, File_C
from blameandshame.localization import Localization


class LocalizationTestCase(unittest.TestCase):

    def check_one(file_name, expected):
        pass        
"""
        loc_res = Localization.from_file(file_name)    
        #self.assertEqual(loc_res, expected)
        self.assertEqual(1,1)
        
    scope = [File_C("File1.java")]
    mapping = {Line_C("File1.java", 3): 0.3,
               Line_C("File1.java", 5): 0.5}
    expected = Localization(mapping, scope)
    
    check_one("filename.yaml", expected)
"""

if __name__ == '__main__':
    unittest.main()
