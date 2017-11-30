import shutil
import os
import git
import urllib.parse
from typing import FrozenSet, Tuple


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


def lines_modified_by_commit(repo: git.Repo,
                             fix_sha: str) -> FrozenSet[Tuple[str, int]]:
    """
    Returns the set of lines that were modified by a given commit. Each line
    is represented by a tuple of the form: (file name, line number).
    """
    # TODO
    raise NotImplementedError

    lines = set()

    diff = prev_commit.diff(fix_commit, create_patch=True)
    for d in diff.iter_change_type('M'):
        print(d.diff)


    return frozenset(lines)
