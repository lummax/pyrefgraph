# coding=utf-8# coding=utf-8
import sys
import types
import typing

from reference_graph import util
from reference_graph import graph as rgraph
from reference_graph.analysis import objects

TraceFunction = typing.Callable[[types.FrameType, str, typing.Any], typing.Any]


class Tracer(util.Setup):
    def __init__(self, graph, object_manager):
        # type: (rgraph.Graph, objects.ObjectManager) -> None
        super(Tracer, self).__init__()
        self._old_trace_function = None  # type: typing.Optional[TraceFunction]
        self.object_manager = object_manager
        self.graph = graph

    def setup(self):
        # type: () -> None
        super(Tracer, self).setup()
        self._old_trace_function = sys.gettrace()
        sys.settrace(self._trace_function)

    def cleanup(self):
        # type: () -> None
        super(Tracer, self).cleanup()
        sys.settrace(self._old_trace_function)  # type: ignore

    def _trace_function(self, frame, event, arg):
        # type: (types.FrameType, str, typing.Any) -> TraceFunction
        if event == "line":
            return self._trace_line(frame)
        if event == "call":
            return self._trace_call(frame)
        if event == "return":
            return self._trace_return(frame, arg)
        if event == "exception":
            return self._trace_exception(frame, *arg)
        return self._trace_function

    def _trace_line(self, frame):
        # type: (types.FrameType) -> TraceFunction
        return self._trace_function

    def _trace_call(self, frame):
        # type: (types.FrameType) -> TraceFunction
        if frame.f_back:
            self.graph.add_call(
                self.object_manager.function_from_frame(frame.f_back.f_code),
                self.object_manager.function_from_frame(frame.f_code),
            )
        else:
            self.graph.add_entry(self.object_manager.function_from_frame(frame.f_code))
        return self._trace_function

    def _trace_return(self, frame, arg):
        # type: (types.FrameType, typing.Any) -> TraceFunction
        # TODO implement
        return self._trace_function

    def _trace_exception(self, frame, exception, value, traceback):
        # type: (types.FrameType, typing.Any, typing.Any, types.TracebackType) -> TraceFunction
        # TODO implement
        return self._trace_function
