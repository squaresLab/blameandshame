from blameandshame.project import Project
from blameandshame.base import Commits
from blameandshame.component import Component
from blameandshame.localization import Localization
import git
from typing import List


class Approach(object):
    """
    An abstract base class for fault localization approaches.
    """
    def __init__(self) -> None:
        raise NotImplementedError

    def localize(self,
                 project: Project,
                 commit: git.Commit,
                 granularity: Component,
                 scope: List[Component]) -> Localization:
        """
        Apply the specific fault localization approach and return a
        Localization object.
        """
        raise NotImplementedError("define localize to use this base class")
