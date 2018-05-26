# coding=utf-8
import sys
import runpy
import pathlib
import typing


class Graph(object):

    @classmethod
    def from_script(cls, path):
        # type: (pathlib.Path) -> Graph
        graph = cls()
        graph.set_trace()
        runpy.run_path(str(path), run_name="__main__")
        return graph

    @classmethod
    def from_module(cls, module):
        # type: (str) -> Graph
        graph = cls()
        graph.set_trace()
        runpy.run_module(module, run_name="__main__", alter_sys=True)
        return graph

    def set_trace(self):
        # type: () -> Graph
        assert not sys.gettrace()
        sys.settrace(self._trace_function)
        return self

    def _trace_function(self, frame, event, arg):
        # type: (frame, str, typing.Any) -> typing.Callable
        return self._trace_function
