# coding=utf-8

import types
import typing

from reference_graph import util
from reference_graph.analysis import graph as rgraph
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
        self._cleanup_callbacks.extend(self._monkey_patch_importlib())
        self._cleanup_callbacks.extend(self._monkey_patch_reload())
        self._cleanup_callbacks.extend(self._monkey_patch_importlib_reload())

    def cleanup(self):
        # type: () -> None
        super(ImportHook, self).cleanup()
        while self._cleanup_callbacks:
            callback = self._cleanup_callbacks.pop(0)
            callback()

    def _process_module(self, imported_module):
        # type: (types.ModuleType) -> None
        for module in self.object_manager.module_from_imported(imported_module):
            # self.graph.add_module(module) -> add edge to imported from TODO
            pass

    def _monkey_patch_import(self):
        old_import_function = util.builtins.__import__

        def cleanup():
            util.builtins.__import__ = old_import_function

        def import_function(name, globals=None, locals=None, fromlist=(), level=0):
            # type: (str, typing.Any, typing.Any, typing.Any, int) -> types.ModuleType
            module = old_import_function(name, globals, locals, fromlist, level)

            if fromlist:
                self._process_module(module)
                for part in fromlist:
                    submodule = getattr(module, part)
                    if submodule and isinstance(submodule, types.ModuleType):
                        self._process_module(submodule)
            else:
                parts = name.split(".")
                current_module = module
                self._process_module(current_module)
                for part in parts[1:]:
                    current_module = getattr(current_module, part)
                    if current_module and isinstance(current_module, types.ModuleType):
                        self._process_module(current_module)
                    else:
                        break
            return module

        util.builtins.__import__ = import_function
        yield cleanup

    def _monkey_patch_importlib(self):
        if hasattr(util.importlib, "import_module"):
            old_importlib_import = util.importlib.import_module

            def cleanup_importlib():
                util.importlib.import_module = old_importlib_import

            def importlib_import_module(name, package=None):
                # type: (str, typing.Any) -> types.ModuleType
                module = old_importlib_import(name, package=package)
                self._process_module(module)
                return module

            util.importlib.import_module = importlib_import_module
            yield cleanup_importlib

    def _monkey_patch_reload(self):
        if hasattr(util.builtins, "reload"):
            old_builtins_reload = util.builtins.reload

            def cleanup_builtins():
                util.builtins.reload = old_builtins_reload

            def builtins_reload(name):
                # type: (str) -> types.ModuleType
                module = old_builtins_reload(name)
                self._process_module(module)
                return module

            util.builtins.reload = builtins_reload
            yield cleanup_builtins

    def _monkey_patch_importlib_reload(self):
        if hasattr(util.importlib, "reload"):
            old_importlib_reload = util.importlib.reload

            def cleanup_importlib():
                util.importlib.reload = old_importlib_reload

            def importlib_reload(name):
                # type: (str) -> types.ModuleType
                module = old_importlib_reload(name)
                self._process_module(module)
                return module

            util.importlib.reload = importlib_reload
            yield cleanup_importlib
