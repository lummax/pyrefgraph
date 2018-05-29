# coding=utf-8
import typing


class Setup(object):
    def __init__(self):
        # type: () -> None
        self._is_setup = False  # type: bool
        self._setup_handlers = list()  # type: typing.List[Setup]

    def _register_setup(self, instance):
        # type: (Setup) -> None
        self._setup_handlers.append(instance)

    def setup(self):
        # type: () -> None
        if self._is_setup:
            raise RuntimeError("Already setup")
        for handler in self._setup_handlers:
            handler.setup()
        self._is_setup = True

    def cleanup(self):
        # type: () -> None
        if not self._is_setup:
            raise RuntimeError("Not setup")
        for handler in self._setup_handlers:
            handler.cleanup()
        self._is_setup = False

    def __enter__(self):
        # type: () -> None
        self.setup()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # type: (typing.Any, typing.Any, typing.Any) -> bool
        self.cleanup()
        return False
