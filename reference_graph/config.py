# coding=utf-8
import argparse
import pathlib
import reference_graph


def parse_args():
    # type: () -> argparse.Namespace
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "entry", help="Entry point script or module for reference " "analysis"
    )
    return parser.parse_args()


def main():
    # type: () -> int
    arguments = parse_args()
    if pathlib.Path(arguments.entry).exists():
        graph = reference_graph.Graph.from_script(arguments.entry)
    else:
        graph = reference_graph.Graph.from_module(arguments.entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
