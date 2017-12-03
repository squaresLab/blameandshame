import shutil
import os
import git
import urllib.parse
from typing import FrozenSet, Tuple, Optional


DESC = "TODO: Add a description of how this tool works."

# Path to the directory used to hold downloaded Git repositories.
REPOS_DIR = os.path.join(os.getcwd(),
                         '.repos')


def repo_path(repo_url: str) -> str:
    """
    Computes the intended path to the local copy of a given repository,
    specified by its URL.
    """
    # get the name of the repo
    path = urllib.parse.urlparse(repo_url).path
    path, ext = os.path.splitext(path)
    _, name = os.path.split(path)

    return os.path.join(REPOS_DIR, name)


def get_repo(repo_url: str) -> git.Repo:
    """
    Returns the GitPython Repo object for a given remote Git repository,
    specified by its URL.

    Internally, this function uses GitPython to clone the entire history for
    Git repositories to disk. Each repository is cloned to its own
    subdirectory within `${PWD}/.repos`.

    Warning: This can potentially consume quite a bit of disk space.
    """
    # Determine the (intended) location of the given repo on disk
    path = repo_path(repo_url)

    # Don't clone the repo if it already exists.
    if not os.path.exists(path):
        try:
            # ensure that the `${PWD}/.repos` directory exists
            if not os.path.exists(REPOS_DIR):
                os.mkdir(REPOS_DIR)

            return git.Repo.clone_from(repo_url, path)

        # ensure that we don't end up with corrupted clones
        except:
            shutil.rmtree(path, ignore_errors=True)
            raise

    return git.Repo(path)


def files_modified_by_commit(repo: git.Repo,
                             fix_sha: str) -> FrozenSet[str]:
    """
    Returns the set of files, given by name, that were modified by a given
    commit.
    """
    fix_commit = repo.commit(fix_sha)
    prev_commit = repo.commit("{}~1".format(fix_sha))
    return frozenset(fix_commit.stats.files.keys())


def authors_of_file(repo: git.Repo,
                    filename: str,
                    since: Optional[git.Commit] = None,
                    until: Optional[git.Commit] = None) -> FrozenSet[str]:
    """
    Returns the set the names of all authors that have modified a file in a
    given repository.

    Params:
      repo: The repository that should be inspected for authorship information.
      filename: The name of the file whose authorship information should be
        obtained.
      since: An optional parameter, used to restrict the consideration of
        authors to all those who modified the file since a particular commit.
        By default, this function will look at all
        commits since the initial commit.
      until: An optional parameter, used to restrict the consideration of
        authors to all those who modified the file up to and including a given
        commit. By default, this function will look at all commits up to and
        including the latest commit.
    """
    raise NotImplementedError


def lines_modified_by_commit(repo: git.Repo,
                             fix_sha: str) -> Tuple[FrozenSet[Tuple[str, int]],
                                                    FrozenSet[Tuple[str, int]]]:
    """
    Returns the set of lines that were modified by a given commit. Each line
    is represented by a tuple of the form: (file name, line number). Two sets
    are created, one containing lines deleted from the old version of the file
    and one containing lines added in the new version of the file. These are
    returned in a tuple of the form (old version, new version).
    """

    old_lines = set()
    new_lines = set()

    fix_commit = repo.commit(fix_sha)
    prev_commit = repo.commit("{}~1".format(fix_sha))

    # unified=0 shows zero lines of context
    diff = prev_commit.diff(fix_commit, create_patch=True, unified=0)
    for d in diff:
        old_file = d.a_path
        new_file = d.b_path

        for line in d.diff.decode('utf8').split('\n'):
            line_tokens = line.split()
            # If the line starts with @@, there's line numbers
            # format: @@ -start,lines +start,lines @@
            first_char = line_tokens[0][0] if len(line_tokens) > 0 else  ''
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
