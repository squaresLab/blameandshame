class Component(object):

    def __init__(self):
        raise NotImplementedError


class File_C(Component):

    def __init__(self,
                 filename: str = "") -> None:
        self.filename = filename


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
                 line_start: int = 0,
                 line_end: int = 0) -> None:
        self.funcname = funcname
        self.filename = filename
        self.line_start = line_start
        self.line_end = line_end
