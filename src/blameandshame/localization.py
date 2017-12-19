from typing import Dict, List
from blameandshame.components import Component
import yaml

VERSION = "1.0"


class Localization (object):

    @staticmethod
    def from_file(filename: str) -> 'Localization':
        """
        Builds a Localization object from a file
        """
        with open(filename) as f:
            try:
                loc = yaml.load(f)
            except KeyError as err:
                print('Error when importing', filename, '.', err)
                raise IOError
        return loc

    def to_file(self, filename: str) -> None:
        """
        Stores its internal data in a file
        """
        with open(filename, "w") as f:
            yaml.dump(self, f)

    def __init__(self,
                 mapping: Dict,
                 scope: List[Component],
                 version: str = VERSION) -> None:

        self.mapping = mapping
        self.scope = scope
        self.__version = version
        self.__granularity = ""

    @property
    def version(self) -> str:
        """
        The version number of this localization object.
        """
        return self.__version

    @property
    def granularity(self) -> str:
        """
        The granularity of this object
        """
        return self.__granularity
