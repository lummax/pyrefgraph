# coding=utf-8
import inspect
import pathlib
import sys
import typing
import types


class Position(object):
    def __init__(self, file, line, column=None):
        # type: (str, int, typing.Optional[int])-> None
        self.file = file
        self.line = line
        self.column = column


class Function(object):
    def __init__(self, code, module):
        # type: (types.CodeType, Module) -> None
        self._code = code
        self.module = module

    @property
    def name(self):
        # type: () -> str
        return self._code.co_name

    @property
    def position(self):
        # type: () -> Position
        return Position(self._code.co_filename, self._code.co_firstlineno)

    def __eq__(self, other):
        # type: (object) -> bool
        return (
            isinstance(other, Function)
            and self.name == other.name
            and self.position == other.position
        )

    def __hash__(self):
        # type: () -> int
        return hash((self.name, self.position))


class Module(object):
    def __init__(self, qualified_name, path):
        # type: (str, typing.Optional[pathlib.Path]) -> None
        self.qualified_name = qualified_name
        self.path = path

    @classmethod
    def from_imported(cls, imported_module):
        # type: (typing.Type[Module], types.ModuleType) -> Module
        source_file = inspect.getsourcefile(imported_module)
        return cls(
            imported_module.__name__,
            pathlib.Path(source_file).resolve() if source_file else None,
        )

    @property
    def name(self):
        return self.qualified_name.split(".")[-1]

    @property
    def qualified_parent(self):
        return self.qualified_name.rpartition(".")[0] or None

    def __eq__(self, other):
        return (
            isinstance(other, Module)
            and other.qualified_name == self.qualified_name
            and other.path == self.path
        )

    def __ne__(self, other):
        return not self == other


class ObjectManager(object):
    def __init__(self):
        self.modules = dict()  # type: typing.Mapping[str, Module]

    def lookup_module(self, qualified_name):
        # type: (str) -> typing.Optional[Module]
        return self.modules.get(qualified_name)

    def function_from_frame(self, function_code):
        # types: (types.CodeType) -> Function
        position = Position(function_code.co_filename, function_code.co_firstlineno)
        module = self.lookup_module(position)
        return Function(function_code, module)

    def module_from_imported(self, imported_module):
        # types: (types.ModuleType) -> Module
        module = Module.from_imported(imported_module)

        if module.qualified_name not in self.modules:
            self.modules[module.qualified_name] = module
        if module.qualified_parent and module.qualified_parent not in self.modules:
            parent = getattr(
                imported_module, "__parent__", sys.modules.get(module.qualified_parent)
            )
            list(self.module_from_imported(parent))  # consume generator

        current_module = module
        while current_module:
            yield current_module
            current_module = self.lookup_module(current_module.qualified_parent)
