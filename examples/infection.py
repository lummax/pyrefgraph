# coding=utf-8
import reference_graph.infection
import sys


class OldStyle:
    pass


class VersionGetter(object):
    def __init__(self):
        self.version = sys.version

    def get_it(self):
        return self.version


def main():
    vg = VersionGetter()
    print(vg.get_it())


if __name__ == "__main__":
    main()
