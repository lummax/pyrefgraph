# coding=utf-8
import argparse
import pathlib
import runpy

import reference_graph


def parse_args():
    # type: () -> argparse.Namespace
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "entry", help="Entry point script or module for reference analysis"
    )
    return parser.parse_args()


def run(arguments):
    # type: (argparse.Namespace) -> int
    with reference_graph.Analysis() as analysis:
        if pathlib.Path(arguments.entry).exists():
            runpy.run_path(arguments.entry, run_name="__main__")
        else:
            runpy.run_module(arguments.entry, run_name="__main__", alter_sys=True)
    return 0


def main():
    # type: () -> int
    return run(parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
