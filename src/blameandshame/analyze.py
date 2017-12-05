import blameandshame.util as util


def analyze_fix_commit(fix_commit: git.Commit) -> dict:
    """
    Collects historical information for a given bug fix, and writes that
    information to disk.

    TODO: Don't use this function to write to disk; splitting data extraction
        and storage into two functions makes testing much easier :-)

    TODO: Assumes that the bug is fixed by a single fix, and not by a sequence
        of successive commits.

    Args:
        fix_commit: Commit object of the bug-fixing commit.
    """
    
    prev_sha = "{}~1".format(commit.hexsha)
    prev_commit = repo.commit(prev_sha)
    fixed_files = list(fix_commit.stats.files.keys())

    # iterate through each file that was modified by the fix commit

    # find the set of lines that were modified by the bug-fix.
    # represented as tuple of the form: (file, line).
    modified_lines = base.lines_modified_by_commit(fix_commit)

    # generate historical information for each modified line
    # TODO
    hist_data = {}

    return hist_data
