from typing import Any, Dict, List
from blameandshame.components import Component, Line_C, Function_C, File_C
import yaml

VERSION = "1.0"

class Localization (object):

    @staticmethod
    def from_file(self, filename: str) -> 'Localization':
        """
        Builds a Localization object from a file
        """
        with open(filename) as f:
            data = yaml.safe_load(f)
            try:
                version = data['version']
                granularity = data['granularity']
                scope = data['scope']
                mapping = data['mapping']

                if granularity == "Line":
                    return LineLocalization(mapping, scope, version)
                if granularity == "Function":
                    return FunctionLocalization(mapping, scope, version)
                if granularity == "File":
                    return FileLocalization(mapping, scope, version)

                # If we don't get a reasonable granularity, raise an exception
                raise IOError
            except KeyError as err:
                print('Error when importing', filename, '.', err)
                raise IOError

    @staticmethod
    def read_mapping(mapping: Dict) -> Dict:
        """
        Builds a Localization objecct from a map
        """
        raise NotImplementedError

    def to_file(self, filename: str) -> None:
        """
        Stores its internal data in a file
        """
        with open(filename, "w") as f:
            data: Dict[str, Any] = dict()
            data['mapping'] = self.mapping
            data['scope'] = self.scope
            data['version'] = self.__version
            data['granularity'] = self.__granularity
            yaml.dump(data, f)

    def __init__(self,
                 mapping: Dict,
                 scope: List[Component],
                 version: str = VERSION,) -> None:

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


class LineLocalization(Localization):

    @staticmethod
    def read_mapping(mapping: Dict[str, Dict[str, str]]
                     ) -> Dict[File_C, Dict[Line_C, float]]:
        """
        Reads in a mapping from a LineLocalization YAML file.

        The dictionary that is returned maps File_C components to dictionaries
        that map Line_C components to scores
        """
        files: Dict[File_C, Dict[Line_C, float]] = dict()
        for file_name, lines in mapping:
            line_mapping: Dict[Line_C, float] = dict()
            for line_number, score in lines:
                line_mapping[Line_C(file_name, int(line_number))] = float(score)
            files[File_C(file_name)] = line_mapping
        return files

    def __init__(self,
                 scope: List[Component],
                 mapping: Dict,
                 version: str) -> None:
        self.scope = scope
        self.mapping = LineLocalization.read_mapping(mapping)
        self.__version = version
        self.__granularity = "Line"


class FunctionLocalization(Localization):

    @staticmethod
    def read_mapping(mapping: Dict[str, Dict[str, str]]
                     ) -> Dict[File_C,
                               Dict[Function_C,
                                    Dict[Line_C, float]]]:
        """
        Reads in a mapping from a FunctionLocalization YAML file.

        The dictionary that is returned maps File_C components to dictionaries
        that map Function_C components to dictionaries that map Line_C
        components to scores.
        """
        files: Dict[File_C,
                    Dict[Function_C,
                         Dict[Line_C, float]]] = dict()

        for file_name, functions in mapping:
            function_mapping: Dict[Function_C, Dict[Line_C, float]] = dict()
            for function_name, lines in functions:
                line_mapping: Dict[Line_C, float] = dict()
                min_line = min(map(int, lines))
                max_line = max(map(int, lines))
                for line_number, score in lines:
                    line_mapping[Line_C(file_name,
                                        int(line_number))] = float(score)
                function_mapping[Function_C(function_name,
                                            File_C(file_name),
                                            min_line,
                                            max_line)] = line_mapping
            files[File_C(file_name)] = function_mapping
        return files

    def __init__(self,
                 scope: List[Component],
                 mapping: Dict,
                 version: str) -> None:
        self.scope = scope
        self.mapping = FunctionLocalization.read_mapping(mapping)
        self.__version = version
        self.__granularity = "Function"


class FileLocalization(Localization):

    @staticmethod
    def read_mapping(mapping: Dict[str, str]) -> Dict[File_C, float]:
        """
        Reads in a mapping from a FileLocalization YAML file.

        The dictionary that is returned maps File_C components to scores.
        """
        files: Dict[File_C, float] = dict()
        for file_name, score in mapping:
            files[File_C(file_name)] = float(score)
        return files

    def __init__(self,
                 scope: List[Component],
                 mapping: Dict,
                 version: str) -> None:
        self.scope = scope
        self.mapping = FileLocalization.read_mapping(mapping)
        self.__version = version
        self.__granularity = "Function"
