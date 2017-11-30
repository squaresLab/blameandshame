#!/usr/bin/env python3
import os
import git
import argparse
import urlparse


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
    path = urlparse.urlparse(repo_url)
    path, ext = os.path.splitext(path)
    _, name = os.path.split(path)

    return os.path.join(REPOS_DIR, name)


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

    # Use GitPython to clone the entire history for the given repository to
    # disk. Repositories are cloned to their own subdirectories within
    # `${PWD}/.repos`.
    #
    # Warning: This can potentially consume quite a bit of disk space!

    # Determine the (intended) location of the given repo on disk
    path = repo_path(repo_url)

    #repo = git.Repo.clone_from()


def build_parser():
    parser = argparse.ArgumentParser(description=DESC)
    return parser


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
