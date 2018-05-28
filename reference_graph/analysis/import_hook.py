# coding=utf-8
import sys
import types
import typing

if sys.version_info[0] >= 3:
    import builtins  # py3
else:
    import __builtin__ as builtins

from reference_graph import util
from reference_graph import graph as rgraph


class ImportHook(util.Setup):

    def __init__(self, graph):
        # type: (rgraph.Graph) -> None
        super(ImportHook, self).__init__()
        self.graph = graph
        self._old_import_function = None  # type: typing.Callable

    def setup(self):
        # type: () -> None
        super(ImportHook, self).setup()
        self._old_import_function = builtins.__import__
        builtins.__import__ = self._import_function

    def cleanup(self):
        # type: () -> None
        super(ImportHook, self).cleanup()
        builtins.__import__ = self._old_import_function

    def _import_function(self, name, *args, **kwargs):
        # type: (str, *typing.Any, **typing.Any) -> types.ModuleType
        module = self._old_import_function(name, *args, **kwargs)
        return module
