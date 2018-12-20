# coding=utf-8
import sys

if sys.version_info[0] >= 3:
    import builtins
    import importlib
else:
    import __builtin__ as builtins
    import imp as importlib

import types
import typing

from reference_graph import util
from reference_graph import graph as rgraph
from reference_graph.analysis import objects


class ImportHook(util.Setup):
    def __init__(self, graph, object_manager):
        # type: (rgraph.Graph, objects.ObjectManager) -> None
        super(ImportHook, self).__init__()
        self.graph = graph
        self.object_manager = object_manager
        self._cleanup_callbacks = list()  # type: typing.List[typing.Callable]

    def setup(self):
        # type: () -> None
        super(ImportHook, self).setup()
        self._cleanup_callbacks.extend(self._monkey_patch_import())
        self._cleanup_callbacks.extend(self._monkey_patch_reload())

    def cleanup(self):
        # type: () -> None
        super(ImportHook, self).cleanup()
        while self._cleanup_callbacks:
            callback = self._cleanup_callbacks.pop(0)
            callback()

    def _process_module(self, name, module):
        # type: (str, types.ModuleType) -> None
        pass

    def _monkey_patch_import(self):
        old_import_function = builtins.__import__

        def cleanup():
            builtins.__import__ = old_import_function

        def import_function(name, *args, **kwargs):
            # type: (str, *typing.Any, **typing.Any) -> types.ModuleType
            module = old_import_function(name, *args, **kwargs)
            self._process_module(name, module)
            return module

        builtins.__import__ = import_function
        yield cleanup

        if hasattr(importlib, "import_module"):
            old_importlib_import = importlib.import_module

            def cleanup_importlib():
                importlib.import_module = old_importlib_import

            def importlib_import_module(name, package=None):
                # type: (str, typing.Any) -> types.ModuleType
                module = old_importlib_import(name, package=package)
                self._process_module(name, module)
                return module

            importlib.import_module = importlib_import_module
            yield cleanup_importlib

    def _monkey_patch_reload(self):
        if hasattr(builtins, "reload"):
            old_builtins_reload = builtins.reload

            def cleanup_builtins():
                builtins.reload = old_builtins_reload

            def builtins_reload(name):
                # type: (str) -> types.ModuleType
                module = old_builtins_reload(name)
                self._process_module(name, module)
                return module

            builtins.reload = builtins_reload
            yield cleanup_builtins

        if hasattr(importlib, "reload"):
            old_importlib_reload = importlib.reload

            def cleanup_importlib():
                importlib.reload = old_importlib_reload

            def importlib_reload(name):
                # type: (str) -> types.ModuleType
                module = old_importlib_reload(name)
                self._process_module(name, module)
                return module

            importlib.reload = importlib_reload
            yield cleanup_importlib
