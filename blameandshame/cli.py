def build_parser():
    parser = argparse.ArgumentParser(description=DESC)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
