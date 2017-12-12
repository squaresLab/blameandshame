import git
from blameandshame.project import Project


class Observation(object):
    """
    Used to represent historical bug fixes.
    """
    @staticmethod
    def build(repo_url: str,
              before_sha: str,
              after_sha: str) -> 'Observation':
        raise NotImplementedError


    def __init__(self,
                 project: Project,
                 before: git.Commit,
                 after: git.Commit):
        self.__project = project
        self.__before = before
        self.__after = after


    @property
    def project(self) -> Project:
        """
        The project that this bug fix occurred in.
        """
        return self.__project


    @property
    def before(self) -> git.Commit:
        """
        The state of the project immediately prior to the bug-fix.
        """
        return self.__before


    @property
    def after(self) -> git.Commit:
        """
        The state of the project immediately after the bug-fix.
        """
        return self.__after
