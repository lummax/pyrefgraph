# coding=utf-8
import inspect
import pathlib
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
    def __init__(self, module, imported_name=None, parent=None):
        # type: (types.ModuleType, typing.Optional[str], typing.Optional[Module]) -> None
        self._module = module
        self._imported_name = imported_name
        self.parent = parent

    @property
    def modulename(self):
        # type: () -> typing.Optional[str]
        return (
            self._imported_name or inspect.getmodulename(str(self.file_path))
            if self.file_path
            else None
        )

    @property
    def file_path(self):
        # type: () -> typing.Optional[pathlib.Path]
        try:
            path = inspect.getsourcefile(self._module)
        except TypeError:
            return None
        return pathlib.Path(path).resolve()


class ObjectManager(object):
    def __init__(self):
        self.modules = dict()  # type: typing.Mapping[str, Module]

    def lookup_module(self, position):
        # type: (Position) -> typing.Optional[Module]
        return self.modules.get(position.file)

    def function_from_frame(self, function_code):
        # types: (types.CodeType) -> Function
        position = Position(function_code.co_filename, function_code.co_firstlineno)
        module = self.lookup_module(position)
        return Function(function_code, module)

    def module_from_import(self, imported_module, imported_name=None):
        # types: (types.ModuleType, typing.Optional[str]) -> Module
        parent = (
            self.module_from_import(imported_module.__parent__)
            if getattr(imported_module, "__parent__", None)
            else None
        )
        module = Module(imported_module, imported_name, parent)
        module_file = module.file_path
        if module_file:
            self.modules[module_file] = module
        return module
