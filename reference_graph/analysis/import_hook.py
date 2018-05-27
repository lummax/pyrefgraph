# coding=utf-8
from reference_graph import util
from reference_graph import graph as rgraph


class ImportHook(util.Setup):

    def __init__(self, graph):
        # type: (rgraph.Graph) -> None
        super(ImportHook, self).__init__()
        self.graph = graph

    def setup(self):
        # type: () -> None
        super(ImportHook, self).setup()

    def cleanup(self):
        # type: () -> None
        super(ImportHook, self).cleanup()
