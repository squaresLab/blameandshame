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
    for (i, line) in enumerate(f.splitlines(), 1):
        line = line.strip()
        row = (i, line)
        tbl.append(row)
    return tbl
