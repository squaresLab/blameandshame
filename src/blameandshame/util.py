import git
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


def last_commit_to_line(repo: git.Repo,
                        filename: str,
                        lineno: int,
                        before: git.Commit) -> Optional[git.Commit]:
    """
    Returns a Commit object corresponding to the last commit where lineno was
    touched before (and including) the Commit object passed in before.
    """
    project = Project(repo)
    try:
        commits = project.commits_to_line(filename, lineno, None, before)
    except git.exc.GitCommandError:
        commits = [None]

    return commits[0]
