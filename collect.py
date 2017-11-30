#!/usr/bin/env python3
import git
import argparse


DESC = "TODO: Add a description of how this tool works."


def build_parser():
    parser = argparse.ArgumentParser(description=DESC)
    return parser


if __name__ == '__main__':
    parser = build_parser()
    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
