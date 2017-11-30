import blameandshame.util as util


def analyze_fix_commit(repo_url: str,
                       fix_sha: str) -> dict:
    """
    Collects historical information for a given bug fix, and writes that
    information to disk.

    TODO: Don't use this function to write to disk; splitting data extraction
        and storage into two functions makes testing much easier :-)

    TODO: Assumes that the bug is fixed by a single fix, and not by a sequence
        of successive commits.

    Args:
        repo_url:   URL of the repository that hosts the fixed program.
        fix_sha:    SHA for the bug-fixing commit.
    """
    repo = util.get_repo(repo_url)
    fix_commit = repo.commit(fix_sha)
    prev_commit = repo.commit("{}~1".format(fix_sha))
    fixed_files = list(fix_commit.stats.files.keys())

    # iterate through each file that was modified by the fix commit

    # find the set of lines that were modified by the bug-fix.
    # represented as tuple of the form: (file, line).
    modified_lines = util.lines_modified_by_commit(repo, fix_sha)

    # generate historical information for each modified line
    # TODO
    hist_data = {}

    return hist_data
