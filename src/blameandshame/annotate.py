from blameandshame.project import Project
from blameandshame.base import Commits
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
      columns: A list of functions, each used to generate a single column of
        annotations. Each function takes as input a Project, a Commit, a
        filename, and a line number and returns a string.
        See column_last_commit for an example.
    """
    if columns is None:
        columns = []
    tbl = []
    f = project.repo.git.show('{}:{}'.format(version.hexsha, filename))

    for (num, line) in enumerate(f.splitlines(), 1):
        line = line.rstrip()
        row = [num, line]

        for col in columns:
            row.append(col(project, version, filename, num))

        tbl.append(tuple(row))

    return tbl


def use_different_commit(f: Callable[[Project, git.Commit, str, int], str],
                         different_commit: git.Commit
                         ) -> Callable[[Project, git.Commit, str, int], str]:
    """
    Returns a modified column function that ignores the commit parameter and
    replaces it with different_commit.
    """
    def modified_fun(p: Project, c: git.Commit, fname: str, l: int) -> str:
        return f(p, different_commit, fname, l)

    return modified_fun


def column_last_commit(project: Project,
                       commit: git.Commit,
                       filename: str,
                       line: int
                       ) -> str:
    """
    Used to provide a column that reports the last commit that touched a given
    version of a file. Does not consider any changes by the provided commit.
    """
    last = project.last_commit_to_line(filename, line, commit)
    return last.hexsha[:7] if last else '-'


def column_num_file_commits_after_modified(project: Project,
                                           commit: git.Commit,
                                           filename: str,
                                           line: int,
                                           ) -> str:
    """
    Reports the number of commits that have been made to a given file since
    a line was modified.
    """
    line_modified_commit = project.last_commit_to_line(filename, line, commit)
    commits = project.commits_to_file(filename, after=line_modified_commit,
                                      before=commit)
    return str(len(commits))


def column_num_project_commits_after_modified(project: Project,
                                              commit: git.Commit,
                                              filename: str,
                                              line: int
                                              ) -> str:
    """
    Reports the number of commits that have been made to a given project
    since a line was modified.
    """
    line_modified_commit = project.last_commit_to_line(filename, line, commit)
    commits = project.commits_to_repo(after=line_modified_commit,
                                      before=commit)
    return str(len(commits))


def column_num_days_since_modified(project: Project,
                                   commit: git.Commit,
                                   filename: str,
                                   line: int
                                   ) -> str:
    """
    Reports the number of days that have passed, relative to a given commit,
    since a given line was last changed.
    """
    return str(project.age_of_line_td(commit, filename, line).days)


def column_was_modified_by_commit(project: Project,
                                  commit: git.Commit,
                                  filename: str,
                                  line: int
                                  ) -> str:
    """
    Returns the string 'Y' if the line was modified by the commit, otherwise
    returns 'N'
    """
    _, new_lines = Project.lines_modified_by_commit(commit)
    for modified_line in new_lines:
        if modified_line.filename == filename and modified_line.num == line:
            return "true"
    return "false"


def column_project_name(project: Project,
                        commit: git.Commit,
                        filename: str,
                        line: int
                        ) -> str:
    """
    Returns the name of the project.
    """
    return project.name


def column_project_age_commits(project: Project,
                               commit: git.Commit,
                               filename: str,
                               line: int
                               ) -> str:
    """
    Returns the age of the project in commits.
    """
    return str(project.age_commits_project(before=commit))


def column_file_age_commits_to_project(project: Project,
                                       commit: git.Commit,
                                       filename: str,
                                       line: int
                                       ) -> str:
    """
    Returns the age of the file in commits to the project.
    """
    return str(project.age_commits_file(filename, Commits.TO_PROJECT,
                                        before=commit))


def column_file_age_commits_to_file(project: Project,
                                    commit: git.Commit,
                                    filename: str,
                                    line: int
                                    ) -> str:
    """
    Returns the age of the file in commits to the file.
    """
    return str(project.age_commits_file(filename, Commits.TO_FILE,
                                        before=commit))
