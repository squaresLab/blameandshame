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


def commits_to_file(repo: git.Repo,
                    filename: str,
                    since: Optional[git.Commit] = None,
                    until: Optional[git.Commit] = None) -> FrozenSet[git.Commit]:
    """
    Returns the set of all commits that been made to a given file, specified by
    its name.

    Params:
      since: An optional parameter used to restrict the search to all commits
        that have occurred since a given commit, inclusive.
      until: An optional parameter used to restrict the search to all commits
        that have occurred upto and including a given commit.
    """
    commits = set()

    if not until:
        until = repo.head.reference.commit

    # BUG: renamed files are given a single entry of the form: "old name -> new name"
    if filename in until.stats.files.keys():
        commits.add(until)

    # TODO: ignore all commits before `since`
    # if the commit renamed the file, stop iterating through the commits
    # that touch files with the current name of the file and instead look
    # at commits since `commit` that touch the file with its original
    # name.
    for commit in until.iter_parents(paths=filename):
        until = commit
        if commit.parents:
            until = commit.parents[0] # TODO: this could break things
            for d in commit.diff(until).iter_change_type('R'):
                if d.rename_to == filename:
                    return frozenset(commits) | \
                           commits_to_file(repo, d.rename_from, since, until)
        commits.add(commit)

    return frozenset(commits)


def commits_to_line(repo: git.Repo,
                    filename: str,
                    lineno: int,
                    since: Optional[git.Commit] = None,
                    until: Optional[git.Commit] = None) -> FrozenSet[git.Commit]:
    """
    Returns the set of commits that have touched a given line in a particular
    file. See `commits_to_file` for more details.

    Params:
        linenno: The one-indexed number of the line in the most recent version
            of the specified file.
    """
    raise NotImplementedError


def authors_of_file(repo: git.Repo,
                    filename: str,
                    since: Optional[git.Commit] = None,
                    until: Optional[git.Commit] = None) -> FrozenSet[git.Actor]:
    """
    Returns the set the names of all authors that have modified a file in a
    given repository. See `commits_to_file` for details about optional
    `since` and `until` parameters.

    Params:
      repo: The repository that should be inspected for authorship information.
      filename: The name of the file, according to `until`, whose authorship
        information should be obtained.
    """
    commits = commits_to_file(repo, filename, since, until)
    return frozenset(c.author for c in commits)


def authors_of_line(repo: git.Repo,
                    filename: str,
                    lineno: int,
                    since: Optional[git.Commit] = None,
                    until: Optional[git.Commit] = None) -> FrozenSet[git.Actor]:
    """
    Returns the set the names of all authors that have modified a specific line
    in a certain file that belongs to a given repository.
    See `authors_of_file` and `commits_to_line` for more details.
    """
    assert lineno > 0

    commits = commits_to_line(repo, filename, lineno, since, until)
    return frozenset(c.author for c in commits)


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
