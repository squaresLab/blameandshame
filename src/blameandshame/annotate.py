from blameandshame.base import Project
from typing import List, Tuple, Any
import git


def annotate(project: Project,
             version: git.Commit,
             filename: str,
             columns = []
             ) -> List[Tuple[Any]]:
    tbl = []
    f = project.repo.git.show('{}:{}'.format(version.hexsha, filename))

    for (num, line) in enumerate(f.splitlines(), 1):
        line = line.strip()
        row = [num, line]

        for col in columns:
            col = col(project, version, filename, num)
            row.append(col)

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
