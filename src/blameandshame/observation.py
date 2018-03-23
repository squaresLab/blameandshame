import csv
import git
from typing import FrozenSet, Generator, List
from blameandshame.project import Project
from blameandshame.base import Line


class Observation(object):
    """
    Used to represent historical bug fixes.
    """
    @staticmethod
    def build(repo_url: str,
              before_sha: str,
              after_sha: str) -> 'Observation':
        project = Project.from_url(repo_url)
        before = project.repo.commit(before_sha)
        after = project.repo.commit(after_sha)
        return Observation(project, before, after)

    def __init__(self,
                 project: Project,
                 before: git.Commit,
                 after: git.Commit) -> None:
        self.__project = project
        self.__before = before
        self.__after = after

    def __str__(self):
        return '{} {}:{}'.format(self.__project, self.__before, self.__after)

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
        were "modified", but those cases are likely to correspond to
        refactoring rather than bug-fixing, and so we should avoid those to
        prevent skewing the model.
        """
        diff = self.before.diff(self.after)
        return frozenset(d.a_path for d in diff.iter_change_type('M'))

    @property
    def modified_lines(self) -> FrozenSet[Line]:
        """
        The set of lines in the buggy version of the project that were modified
        as part of the bug fix. Note that lines belonging to files that were
        deleted by the bug fix are not considered to have been modified.
        """
        files = list(self.modified_files)
        return Project.lines_modified_between_commits(before=self.before,
                                                      after=self.after,
                                                      in_files=files)


class ObservationCollection(Generator):
    def __init__(self, filename: str) -> None:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            # skip header
            next(reader, None)
            observations = list(reader)
        self.__observations = iter(observations)

    def send(self, _) -> Observation:
        while True:
            try:
                repo_url, bug_sha, _, fix_sha, _ = next(self.__observations)
                return Observation.build(repo_url, bug_sha, fix_sha)
            except ValueError:
                pass

    def throw(self, type=None, value=None, traceback=None) -> None:
        raise StopIteration

    def save(self, fn: str) -> None:
        # with open(fn, 'w') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(["Repository URL",
        #                      "Bug Commit",
        #                      "Bug Build URL",
        #                      "Fix Commit",
        #                      "Fix Build URL"])
        #     for observation in self.__observations:
        #         row = [observation.repository,
        #                observation.commit_bug,
        #                observation.build_url_bug,
        #                observation.commit_fix,
        #                observation.build_url_fix]
        #         writer.writerow(row)
        raise NotImplementedError
