# coding=utf-8
import sys
import reference_graph.api

graph = reference_graph.api.run() \
    if not sys.gettrace() else None
