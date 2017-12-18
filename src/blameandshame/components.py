from typing import Dict, FrozenSet, List, Tuple, Optional, Set


class Component(object):

    def __init__(self):
        raise NotImplementedError


class File_C(Component):

    def __init__(self,
                 filename: str = "") -> None:
        self.file_name = filename


class Line_C(Component):

    def __init__(self,
                 filename: str = "",
                 lineno: int = 0) -> None:
        self.filename = filename
        self.lineno = lineno


class Function_C(Component):

    def __init__(self,
                 funcname: str = "",
                 filename: File_C = None,
                 linestart: int = 0,
                 lineend: int = 0) -> None:
        self.func_name = funcname
        self.filename = filename
        self.line_start = linestart
        self.line_end = lineend
