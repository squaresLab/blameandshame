from enum import Enum
from typing import FrozenSet, List, Tuple, Optional, Set
import git
import os
import shutil
import urllib.parse
from datetime import timedelta


class Change(Enum):
    """
    Enum of the possible types of git changes. These values can be used as
    arguments to the Diff object's iter_change_type method.
    """
    ADDED = 'A'
    DELETED = 'D'
    MODIFIED = 'M'
    RENAMED = 'R'


class Project(object):

    # Path to the directory used to hold downloaded Git repositories.
    REPOS_DIR = os.path.join(os.getcwd(), '.repos')

    @staticmethod
    def _url_to_path(url: str) -> str:
        """
        Computes the intended path to the local copy of a given project,
        specified by the URL of its repository.
        """
        # get the name of the repo
        path = urllib.parse.urlparse(url).path
        path, _ = os.path.splitext(path)
        _, name = os.path.split(path)

        return os.path.join(Project.REPOS_DIR, name)

    @staticmethod
    def from_url(url: str) -> 'Project':
        """
        Retrieves a project by the URL of its Git repository.

        Internally, this function uses GitPython to clone the entire history
        for Git repositories to disk. Each repository is cloned to its own
        subdirectory within `${PWD}/.repos`.

        Warning: This can potentially consume quite a bit of disk space.
        """
        # Determine the (intended) location of the given repo on disk
        path = Project._url_to_path(url)

        # Don't clone the repo if it already exists.
        if not os.path.exists(path):
            try:
                # ensure that the `${PWD}/.repos` directory exists
                if not os.path.exists(Project.REPOS_DIR):
                    os.mkdir(Project.REPOS_DIR)

                repo = git.Repo.clone_from(url, path)
                return Project(repo)

            # ensure that we don't end up with corrupted clones
            except git.exc.GitCommandError:
                shutil.rmtree(path, ignore_errors=True)
                raise

        return Project.from_disk(path)

    @staticmethod
    def from_disk(path: str) -> 'Project':
        """
        Retrieves a project whose repository is stored at a given local path.
        """
        return Project(git.Repo(path))

    def __init__(self, repo: git.Repo) -> None:
        self.__repo: git.Repo = repo
        self.update()

    def update(self):
        """
        Updates the state of the Git repository associated with this project.
        """
        self.repo.remotes.origin.pull()

    @property
    def repo(self) -> git.Repo:
        """
        The Git repository associated with this project.
        """
        return self.__repo

    def files_in_commit(self,
                        fix_commit: git.Commit,
                        filter_by: Set[Change] = {f for f in Change}
                        ) -> FrozenSet[str]:
        """
        Returns the set of files, given by name, that were modified by a
        specified commit.
        """
        prev_sha = "{}~1".format(fix_commit.hexsha)
        prev_commit = fix_commit.repo.commit(prev_sha)
        diff = prev_commit.diff(fix_commit)

        files: Set[str] = set()
        for f in filter_by:
            files.update(d.a_path for d in diff.iter_change_type(f.value))

        return frozenset(files)

    def commits_to_repo(self,
                        after: Optional[git.Commit] = None,
                        before: Optional[git.Commit] = None,
                        ) -> List[git.Commit]:
        """
        Returns a list of all commits that have been made to the repo.

        Params:
          after: An optional parameter used to restrict the search to all
            commits that have occurred since a given commit, inclusive.
          before: An optional parameter used to restrict the search to all
            commits that have occurred up to and including a given commit.
        """
        if not before:
            before = self.repo.head.reference.commit

        rev_range = '{}^..{}'.format(after, before) if after else before.hexsha

        log = self.repo.git.log(rev_range)
        commit_hashes = \
            [l.strip() for l in log.splitlines() if l.startswith('commit ')]
        commits = [self.repo.commit(l[7:]) for l in commit_hashes]
        return commits

    def commits_to_file(self,
                        filename: str,
                        lineno: Optional[int] = None,
                        after: Optional[git.Commit] = None,
                        before: Optional[git.Commit] = None
                        ) -> List[git.Commit]:
        """
        Returns the set of all commits that been made to a given file,
        specified by its name.

        Params:
          after: An optional parameter used to restrict the search to all
            commits that have occurred since a given commit, inclusive.
          before: An optional parameter used to restrict the search to all
            commits that have occurred up to and including a given commit.
        """
        assert lineno is None or lineno > 0

        # construct the range of revisions that should be searched
        if not before:
            before = self.repo.head.reference.commit

        rev_range = '{}^..{}'.format(after, before) if after else before.hexsha

        # construct the range of lines that should be searched
        if lineno is None:
            log = self.repo.git.log(rev_range, '--follow', '--', filename)
        else:
            line_range = '{},{}:{}'.format(lineno, lineno, filename)
            log = self.repo.git.log(rev_range, L=line_range)

        # read the commit hashes from the log
        commit_hashes = \
            [l.strip() for l in log.splitlines() if l.startswith('commit ')]
        commits = [self.repo.commit(l[7:]) for l in commit_hashes]
        return commits

    def commits_to_function(self,
                            filename: str,
                            regex: str,
                            after: Optional[git.Commit] = None,
                            before: Optional[git.Commit] = None,
                            ) -> List[git.Commit]:
        """
        Returns a list of all commits that have been made to the repo.

        Params:
          filename: The file containing the function.
          regex: A string corresponding to the regex matching the function.
          after: An optional parameter used to restrict the search to all
            commits that have occurred since a given commit, inclusive.
          before: An optional parameter used to restrict the search to all
            commits that have occurred up to and including a given commit.
        """
        raise NotImplementedError

    def commits_to_line(self,
                        filename: str,
                        lineno: int,
                        after: Optional[git.Commit] = None,
                        before: Optional[git.Commit] = None
                        ) -> List[git.Commit]:
        """
        Returns the set of commits that have touched a given line in a
        particular file. See `commits_to_file` for more details.

        Params:
            linenno: The one-indexed number of the line in the most recent
              version of the specified file.
        """
        return self.commits_to_file(filename,
                                    lineno=lineno,
                                    after=after,
                                    before=before)

    def authors_of_file(self,
                        filename: str,
                        after: Optional[git.Commit] = None,
                        before: Optional[git.Commit] = None
                        ) -> FrozenSet[git.Actor]:
        """
        Returns the set the names of all authors that have modified a file in a
        given repository. See `commits_to_file` for details about optional
        `after` and `before` parameters.

        Params:
          repo: The repository that should be inspected for authorship
            information.
          filename: The name of the file, according to `before`, whose
            authorship information should be obtained.
        """
        commits = self.commits_to_file(filename, after=after, before=before)
        return frozenset(c.author for c in commits)

    def last_commit_to_line(self,
                            filename: str,
                            lineno: int,
                            before: git.Commit
                            ) -> Optional[git.Commit]:
        """
        Returns a Commit object corresponding to the last commit where lineno
        was touched before (and including) the Commit object passed in before.
        """
        try:
            commits = self.commits_to_line(filename, lineno, None, before)
        except git.exc.GitCommandError:
            commits = [None]

        return commits[0]

    def lines_modified_by_commit(self,
                                 fix_commit: git.Commit
                                 ) -> Tuple[FrozenSet[Tuple[str, int]],
                                            FrozenSet[Tuple[str, int]]]:
        """
        Returns the set of lines that were modified by a given commit. Each
        line is represented by a tuple of the form: (file name, line number).
        Two sets are created, one containing lines deleted from the old version
        of the file and one containing lines added in the new version of the
        file. These are returned in a tuple of the form (old version, new
        version).
        """
        old_lines = set()
        new_lines = set()

        prev_sha = "{}~1".format(fix_commit.hexsha)
        prev_commit = fix_commit.repo.commit(prev_sha)

        # unified=0 shows zero lines of context
        diff = prev_commit.diff(fix_commit, create_patch=True, unified=0)
        for d in diff:
            old_file = d.a_path
            new_file = d.b_path

            for line in d.diff.decode('utf8').split('\n'):
                line_tokens = line.split()
                # If the line starts with @@, there's line numbers
                # format: @@ -start,lines +start,lines @@
                first_char = line_tokens[0][0] if len(line_tokens) > 0 else ''
                if (first_char == '@'):
                    _, old_line_num, new_line_num, *_ = line_tokens
                    old_line_num = int(old_line_num[1:].split(',')[0])
                    new_line_num = int(new_line_num[1:].split(',')[0])
                elif (first_char == '-'):
                    old_lines.add((old_file, old_line_num))
                    old_line_num += 1
                elif (first_char == '+'):
                    new_lines.add((new_file, new_line_num))
                    new_line_num += 1
                else:
                    old_line_num += 1
                    new_line_num += 1

        return (frozenset(old_lines), frozenset(new_lines))

    def authors_of_line(self,
                        filename: str,
                        lineno: int,
                        after: Optional[git.Commit] = None,
                        before: Optional[git.Commit] = None
                        ) -> FrozenSet[git.Actor]:
        """
        Returns the set the names of all authors that have modified a specific
        line in a certain file that belongs to a given repository.
        See `authors_of_file` and `commits_to_line` for more details.
        """
        assert lineno > 0

        commits = self.commits_to_line(filename,
                                       lineno,
                                       after=after,
                                       before=before)
        return frozenset(c.author for c in commits)

    def time_between_commits(self,
                             x: git.Commit,
                             y: git.Commit
                             ) -> timedelta:
        """
        Given two commits, this function should return the length of time
        between them as a timedelta.
        def time_between_commits(x: git.Commit, y: git.Commit) -> timedelta:
        This function can be combined with last_commit_to_line to determine the
        length of time since the last change to a faulty line.
        """
        timeX = x.authored_datetime
        timeY = y.authored_datetime
        return timeX - timeY
