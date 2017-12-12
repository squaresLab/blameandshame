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


    @property
    def modified_files(self) -> FrozenSet[str]:
        """
        The set of files that were modified as part of the bug fix, given by
        their names in the buggy version of the project. Files that were added
        or deleted as part of the bug fix are not considered to be "modified".
        We do not include the names of files that were added, not only because
        they do not exist in the buggy version of the project, but because they
        contain no information relevant to fault localization. We could include
        files that were deleted by simply considering that all of their lines
        were "modified", but those cases are likely to correspond to refactoring
        rather than bug-fixing, and so we should avoid those to prevent skewing
        the model.
        """
        raise NotImplementedError
