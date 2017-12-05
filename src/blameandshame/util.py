from blameandshame.base import Change, Project
from typing import FrozenSet, List, Tuple, Optional, Set


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

    commits = commits_to_line(repo, filename, lineno, since=since, until=until)
    return frozenset(c.author for c in commits)
