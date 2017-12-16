from blameandshame.project import Project
from blameandshame.base import Commits
# from blameandshame.component import Component
# from blameandshame.localization import Localization
import git
from typing import List


class Component():
    """
    Stub Component. Delete and uncomment the import above when the full
    version is complete
    """
    pass


class Localization():
    """
    Stub Localization. Delete and uncomment the import above when the full
    version is complete
    """
    pass


class Approach(object):
    """
    An abstract base class for fault localization approaches.
    """
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
