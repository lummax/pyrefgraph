# coding=utf-8

from reference_graph import util
from reference_graph.analysis import graph as rgraph
from reference_graph.analysis import tracer, objects
from reference_graph.analysis import import_hook


class Analysis(util.Setup):
    def __init__(self, graph=None):
        super(Analysis, self).__init__()
        self.graph = graph or rgraph.Graph()
        self.object_manager = objects.ObjectManager()
        self.tracer = self._register_setup(
            tracer.Tracer(self.graph, self.object_manager)
        )
        self.import_hook = self._register_setup(
            import_hook.ImportHook(self.graph, self.object_manager)
        )
