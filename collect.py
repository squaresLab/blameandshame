#!/usr/bin/env python3
import shutil
import os
import git
import argparse
import urllib.parse


DESC = "TODO: Add a description of how this tool works."

# Path to the directory used to hold downloaded Git repositories.
REPOS_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)),
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


def analyze_fix_commit(repo_url: str,
                       fix_sha: str) -> None:
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
    repo = get_repo(repo_url)
    fix_commit = repo.commit(fix_sha)
    prev_commit = repo.commit("{}~1".format(fix_sha))
    fixed_files = list(fix_commit.stats.files.keys())

    # iterate through each file that was modified by the fix commit
    diff = prev_commit.diff(fix_commit, create_patch=True)
    for d in diff.iter_change_type('M'):
        print(d.diff)
        # print("A blob:\n{}".format(d.a_blob.data_stream.read().decode('utf-8')))


def build_parser():
    parser = argparse.ArgumentParser(description=DESC)
    return parser


if __name__ == '__main__':
    # parser = build_parser()
    # args = parser.parse_args()
    # if 'func' in args:
    #     args.func(args)

    analyze_fix_commit('https://github.com/google/protobuf', '74f64b6')
