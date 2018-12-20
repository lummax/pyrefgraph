# coding=utf-8
import typing

from reference_graph.analysis import objects


class Node(object):
    def __init__(self, *args, **kwargs):
        pass


class FunctionNode(Node):
    pass


class ModuleNode(Node):
    pass


class Edge(object):
    def __init__(self, *args, **kwargs):
        pass


class CallEdge(Edge):
    pass


class ImportEdge(Edge):
    pass


NodeType = typing.TypeVar("NodeType", bound=Node)
EdgeType = typing.TypeVar("EdgeType", bound=Edge)


class Graph(object):
    def add_node(self, node):
        # type (Type[NodeType]) -> NodeType
        return node  # TODO actually insert

    def add_edge(self, edge):
        # type (Type[EdgeType]) -> EdgeType
        return edge  # TODO actually insert

    def add_function(self, function):
        # type: (objects.Function) -> FunctionNode
        return self.add_node(FunctionNode(function))

    def add_entry(self, function):
        # type: (objects.Function) -> FunctionNode
        node = self.add_node(FunctionNode(function))  # TODO mark entry
        return node

    def add_call(self, caller, callee):
        # type: (objects.Function, objects.Function) -> CallEdge
        return self.add_edge(
            CallEdge(self.add_function(caller), self.add_function(callee))
        )

    def add_module(self, module):
        # type: (objects.Module) -> ModuleNode
        return self.add_node(ModuleNode(module))

    def add_import(self, origin, module):
        # type: (objects.Module, objects.Module) -> ImportEdge
        return self.add_edge(
            ImportEdge(self.add_module(origin), self.add_module(module))
        )
