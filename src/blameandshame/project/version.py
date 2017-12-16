import git
from blameandshame.project.base import Project


class ProjectVersion(object):
    """
    Used to represent the version of a particular project associated with a
    given commit.
    """

    def __init__(self,
                 project: Project,
                 commit: git.Commit
                 ) -> None:
        self.__project = project
        self.__commit = commit

    @property
    def project(self) -> Project:
        return self.__project

    @property
    def commit(self) -> git.Commit:
        return self.__commit
