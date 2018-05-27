# coding=utf-8# coding=utf-8
import sys
import types
import typing

from reference_graph import util
from reference_graph import graph as rgraph


TraceFunction = typing.Callable[[types.FrameType, str, typing.Any], typing.Any]


class Tracer(util.Setup):

    def __init__(self, graph):
        # type: (rgraph.Graph) -> None
        super(Tracer, self).__init__()
        self._old_trace_function = None  # type: typing.Optional[TraceFunction]
        self.graph = graph

    def setup(self):
        # type: () -> None
        super(Tracer, self).setup()
        self._old_trace_function = sys.gettrace()
        sys.settrace(self._trace_function)

    def cleanup(self):
        # type: () -> None
        super(Tracer, self).cleanup()
        sys.settrace(self._old_trace_function)

    def _trace_function(self, frame, event, arg):
        # type: (types.FrameType, str, typing.Any) -> TraceFunction
        return self._trace_function
