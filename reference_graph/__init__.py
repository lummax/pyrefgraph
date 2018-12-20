# coding=utf-8

from reference_graph.analysis.graph import Graph
from reference_graph.analysis import Analysis


def infect(graph=None):
    # type: (Graph) -> Analysis
    analysis = Analysis(graph)
    analysis.setup()
    return analysis
