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

    def provision(self) -> 'bugzoo.Container':
        """
        Provisions a fresh BugZoo container for this project version.
        """
        raise NotImplementedError

    @property
    def tests(self) -> 'bugzoo.testing.TestSuite':
        """
        The test suite used by this project version.
        """
        # TODO: The TestSuite class should be provided by BugZoo. It's
        #   likely that the existing TestSuite class within BugZoo doesn't
        #   quite meet our needs; in that case, we should modify and extend
        #   it.
        raise NotImplementedError

    @property
    def coverage(self) -> 'bugzoo.coverage.ProjectLineCoverage':
        """
        The line coverage achieved by each test within the test suite for this
        project version.
        """
        raise NotImplementedError

        # TODO
        # determine the location of the coverage file(s) on disk

        # TODO
        # If possible, read existing coverage information from disk.

        try:
            # TODO: provision container for program version
            container = self.provision()

            # TODO: attempt to compile the program inside the container
            container.compile() # mode=CompliationMode.COVERAGE

            # TODO: collect coverage information for the entire test suite
            coverage = container.coverage()

            # TODO: save coverage to disk
            #
        finally:
            if container:
                container.destroy()
