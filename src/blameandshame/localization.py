from typing import Dict, List
from blameandshame.components import Component, Line_C, Function_C, File_C
import yaml


class Localization (object):

    mapping = dict()
    scope = []

    def __init__(self, mapping: dict = {}, scope: list = []):
        self.mapping = mapping
        self.scope = scope

    def add_comp_score(self, comp: Component, score: float) -> None:
        """
        Adds a component and its respective score to the mapping
        of localizations
        """
        self.mapping[comp] = score
        
    def set_scope(self, scope: list = []):
        """
        Sets a list of File_C as the scope list
        """
        self.scope = scope
        
    def add_file_to_scope(self, filename: File_C):
        """
        Adds a file to the scope list
        """
        self.scope.append(filename)

    @staticmethod
    def from_file(self, filename: str) -> 'Localization':
        """
        Builds a Localization object from a file
        """
        with open(filename) as f:
            data_map = yaml.safe_load(f)
            loc = map_to_loc(data_map) 
        return loc

    #@abstractmethod
    def map_to_loc(self, data_map: map = {}) -> 'Localization':
        """
        Builds a Localization objecct from a map
        """
        pass

    def to_file(self, filename: str) -> None:
        """
        Stores its internal data in a file
        """
        with open(filename, "w") as f:
            data_map = build_map()
            yaml.dump(data_map, f)

    #@abstractmethod
    def build_map(self) -> map:
        """
        Builds a map in the proper format to be stored in a YAML file
        """
        pass


class Line_Localization(Localization):

    def map_to_loc(self, data_map: map = {}) -> Localization:
        """
        Builds a Localization objecct from a map 
        """
        sco_list = data_map['scope']
        loc_dic = data_map['localization']
        
        loc = Localization()

        for sco_file in sco_list:
            loc.add_file_to_scope(sco_file)

        for filename in loc_dic.keys():
            for line in loc_dic[filename].keys():
                l = Line_C(filename,loc_dic[filename])
                loc.add_comp_score(l, loc_dic[filename][line])
        
        return loc

    def build_map(self) -> map:
        """
        Builds a map of a line in yaml format to be stored in a YAML file
        """
        ret = {}
        ret['version'] = "1.0"
        ret['granularity'] = "line" 
        ret['scope'] = [x for x in self.scope]
        
        files_to_lines = {}
        files_list = [linec.filename for linec in mapping.keys()]
        files_set = set(files_list)
        for files in files_set:
            line_map = {}
            for linec in mapping.keys():
                if linec.filename == files:
                    line_map[linec.lineno] = mapping[linec]
            files_to_lines[files] = line_map
        ret['localization'] = files_to_lines

class Function_Localization(Localization):

    def map_to_loc(self, data_map: map = {}) -> Localization:
        """
        Builds a Localization objecct from a map 
        """
        pass

    def build_map(self) -> map:
        """
        Builds a map of a func to be stored in a YAML file
        """
        pass


class File_Localization(Localization):

    def map_to_loc(self, data_map: map = {}) -> Localization:
        """
        Builds a Localization objecct from a map 
        """
        pass

    def build_map(self) -> map:
        """
        Builds a map of a file to be stored in a YAML file
        """
        pass
