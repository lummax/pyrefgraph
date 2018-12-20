# coding=utf-8
import sys


class OldStyle:
    pass


class VersionGetter(object):
    def __init__(self):
        self.version = sys.version

    def get_it(self):
        return self.version


def exception():
    raise RuntimeError("foo")


def main():
    vg = VersionGetter()
    print(vg.get_it())

    try:
        exception()
    except RuntimeError:
        pass


if __name__ == "__main__":
    main()
