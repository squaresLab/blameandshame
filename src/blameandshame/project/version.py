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
        """
        The project associated with this version.
        """
        return self.__project

    @property
    def commit(self) -> git.Commit:
        """
        The commit associated with this version of the project.
        """
        return self.__commit

    @property
    def tests(self) -> 'TestSuite':
        """
        The test suite used by this project version.
        """
        raise NotImplementedError
