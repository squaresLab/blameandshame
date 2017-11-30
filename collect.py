#!/usr/bin/env python3
import git
import argparse


DESC = "TODO: Add a description of how this tool works."


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
    print('hello')


def build_parser():
    parser = argparse.ArgumentParser(description=DESC)
    return parser


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
