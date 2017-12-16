from enum import Enum, auto


class Line(object):
    """
    Represents a single line in a given file.
    """
    def __init__(self, filename: str, num: int) -> None:
        assert num > 0
        self.__filename = filename
        self.__num = num

    @property
    def filename(self) -> str:
        """
        The name of the file to which this line belongs.
        """
        return self.__filename

    @property
    def num(self) -> int:
        """
        The one-indexed number of the line.
        """
        return self.__num

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return "{}:{}".format(self.__filename, self.__num)

    def __eq__(self, other) -> bool:
        return isinstance(other, Line) \
               and other.filename == self.filename \
               and other.num == self.num

    def __hash__(self) -> int:
        return hash((self.__filename, self.__num))


class Change(Enum):
    """
    Enum of the possible types of git changes. These values can be used as
    arguments to the Diff object's iter_change_type method.
    """
    ADDED = 'A'
    DELETED = 'D'
    MODIFIED = 'M'
    RENAMED = 'R'


class Commits(Enum):
    TO_PROJECT = auto()
    TO_FILE = auto()
    TO_LINE = auto()
