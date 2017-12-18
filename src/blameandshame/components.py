from typing import Dict, FrozenSet, List, Tuple, Optional, Set


class Component(object):

    def __init__(self):
        pass


class File_C(Component):

    file_name = ""

    def __init__(self, filename: str = ""):
        self.file_name = filename


class Line_C(Component):

    lineno = 0
    filename = ""

    def __init__(self, filename: str = "", lineno: int = 0):
        self.filename = filename
        self.lineno = lineno


class Function_C(Component):
    
    filename = None
    func_name= ""
    line_start = 0
    line_end = 0
    
    def __init__(self, funcname: str = "", filename: File_C = None,
                 linestart: int = 0, lineend: int = 0):
        self.func_name = funcname
        self.filename = filename
        self.line_start = linestart
        self.line_end = lineend

