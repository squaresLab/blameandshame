from blameandshame.base import Project
from typing import Callable, Optional, List, Tuple, Any
import git


def annotate(project: Project,
             version: git.Commit,
             filename: str,
             columns: Optional[List[
                        Callable[[Project, git.Commit, str, int], str]
                      ]] = None
             ) -> List[Tuple[Any, ...]]:
    """
    Returns a list of tuples corresponding to a table of annotated values.

    Params:
      columns: A list of functions used to generate a column of data. Each
        function takes as input a Project, a Commit, a filename, and a line
        number and returns a string. See column_last_commit for an example.
    """
    if columns is None:
        columns = []
    tbl = []
    f = project.repo.git.show('{}:{}'.format(version.hexsha, filename))

    for (num, line) in enumerate(f.splitlines(), 1):
        line = line.strip()
        row = [num, line]

        for col in columns:
            row.append(col(project, version, filename, num))

        tbl.append(tuple(row))

    return tbl


def column_last_commit(project : Project,
                       commit: git.Commit,
                       filename : str,
                       line : int
                       ) -> str:
    """
    Used to provide a column that reports the last commit that touched a given
    version of a file. Does not consider any changes by the provided commit.
    """
    last = project.last_commit_to_line(filename, line, commit)
    return last.hexsha[:7] if last else '-'
