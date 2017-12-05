from enum import Enum
from typing import FrozenSet, List, Tuple, Optional, Set
import git
import os
import shutil
import urllib.parse


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
        path, ext = os.path.splitext(path)
        _, name = os.path.split(path)

        return os.path.join(Project.REPOS_DIR, name)


    @staticmethod
    def from_url(url: str) -> 'Project':
        """
        Retrieves a project by the URL of its Git repository.

        Internally, this function uses GitPython to clone the entire history for
        Git repositories to disk. Each repository is cloned to its own
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
            except:
                shutil.rmtree(path, ignore_errors=True)
                raise

        return Project.from_disk(path)


    @staticmethod
    def from_disk(path: str) -> 'Project':
        """
        Retrieves a project whose repository is stored at a given local path.
        """
        return Project(git.Repo(path))


    def __init__(self, repo: git.Repo):
        self.__repo : git.Repo = repo
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
                        fix_sha: str,
                        filter_by: Set[Change] = {f for f in Change}
                       ) -> FrozenSet[str]:
        """
        Returns the set of files, given by name, that were modified by a
        specified commit.
        """
        fix_commit = self.repo.commit(fix_sha)
        prev_commit = self.repo.commit("{}~1".format(fix_sha))
        diff = prev_commit.diff(fix_commit)

        files: Set[str] = set()
        for f in filter_by:
            files.update(d.a_path for d in diff.iter_change_type(f.value))

        return frozenset(files)


    def commits_to_file(self,
                        filename: str,
                        lineno: Optional[int] = None,
                        since: Optional[git.Commit] = None,
                        until: Optional[git.Commit] = None
                        ) -> List[git.Commit]:
        """
        Returns the set of all commits that been made to a given file, specified by
        its name.

        Params:
          since: An optional parameter used to restrict the search to all commits
            that have occurred since a given commit, inclusive.
          until: An optional parameter used to restrict the search to all commits
            that have occurred upto and including a given commit.
        """
        assert lineno is None or lineno > 0

        # construct the range of revisions that should be searched
        if not until:
            until = self.repo.head.reference.commit
        if not since:
            rev_range = until.hexsha
        else:
            rev_range = '{}^..{}'.format(since, until)

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


    def commits_to_line(self,
                        filename: str,
                        lineno: int,
                        since: Optional[git.Commit] = None,
                        until: Optional[git.Commit] = None
                        ) -> List[git.Commit]:
        """
        Returns the set of commits that have touched a given line in a particular
        file. See `commits_to_file` for more details.

        Params:
            linenno: The one-indexed number of the line in the most recent version
                of the specified file.
        """
        return self.commits_to_file(filename,
                                    lineno=lineno,
                                    since=since,
                                    until=until)


    def authors_of_file(self,
                        filename: str,
                        since: Optional[git.Commit] = None,
                        until: Optional[git.Commit] = None
                        ) -> FrozenSet[git.Actor]:
        """
        Returns the set the names of all authors that have modified a file in a
        given repository. See `commits_to_file` for details about optional
        `since` and `until` parameters.

        Params:
          repo: The repository that should be inspected for authorship information.
          filename: The name of the file, according to `until`, whose authorship
            information should be obtained.
        """
        commits = self.commits_to_file(filename, since=since, until=until)
        return frozenset(c.author for c in commits)


    def last_commit_to_line(self,
                            filename: str,
                            lineno: int,
                            before: git.Commit
                            ) -> Optional[git.Commit]:
        """
        Returns a Commit object corresponding to the last commit where lineno was
        touched before (and including) the Commit object passed in before.
        """
        try:
            commits = self.commits_to_line(filename, lineno, None, before)
        except git.exc.GitCommandError:
            commits = [None]

        return commits[0]
