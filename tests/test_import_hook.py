# coding=utf-8
import pytest

from reference_graph.util import builtins, importlib
from reference_graph.analysis import import_hook, objects, graph


class ImportImportHook(import_hook.ImportHook):
    def setup(self):
        super(import_hook.ImportHook, self).setup()
        self._cleanup_callbacks.extend(self._monkey_patch_import())


class ImportLibImportHook(import_hook.ImportHook):
    def setup(self):
        super(import_hook.ImportHook, self).setup()
        self._cleanup_callbacks.extend(self._monkey_patch_importlib())


def test_setup_cleanup():
    def get_values():
        return (
            builtins.__import__,
            getattr(importlib, "import_module", None),
            getattr(builtins, "reload", None),
            getattr(importlib, "reload", None),
        )

    old = get_values()
    hook = import_hook.ImportHook(None, None)
    hook.setup()
    hook.cleanup()
    assert get_values() == old

    with import_hook.ImportHook(None, None):
        pass
    assert get_values() == old


def test_basic_import():
    om = objects.ObjectManager()
    with ImportImportHook(graph.Graph(), om):
        import this

    assert om.lookup_module("this") == objects.Module.from_imported(this)


def test_nested_import():
    om = objects.ObjectManager()
    with ImportImportHook(graph.Graph(), om):
        import email.mime.message

    assert om.lookup_module("email") == objects.Module.from_imported(email)
    assert om.lookup_module("email.mime") == objects.Module.from_imported(email.mime)
    assert om.lookup_module("email.mime.message") == objects.Module.from_imported(
        email.mime.message
    )


def test_from_import():
    om = objects.ObjectManager()
    with ImportImportHook(graph.Graph(), om):
        from email.mime import message

    import email.mime

    assert om.lookup_module("email") == objects.Module.from_imported(email)
    assert om.lookup_module("email.mime") == objects.Module.from_imported(email.mime)
    assert om.lookup_module("email.mime.message") == objects.Module.from_imported(
        email.mime.message
    )


def test_from_import_with_nonmodule():
    om = objects.ObjectManager()
    with ImportImportHook(graph.Graph(), om):
        from email.mime.message import MIMEMessage

    import email.mime

    assert om.lookup_module("email") == objects.Module.from_imported(email)
    assert om.lookup_module("email.mime") == objects.Module.from_imported(email.mime)
    assert om.lookup_module("email.mime.message") == objects.Module.from_imported(
        email.mime.message
    )


def test_complex_from_import():
    om = objects.ObjectManager()
    with ImportImportHook(graph.Graph(), om):
        from email.mime import message, image

    import email.mime

    assert om.lookup_module("email") == objects.Module.from_imported(email)
    assert om.lookup_module("email.mime") == objects.Module.from_imported(email.mime)
    assert om.lookup_module("email.mime.message") == objects.Module.from_imported(
        email.mime.message
    )
    assert om.lookup_module("email.mime.image") == objects.Module.from_imported(
        email.mime.image
    )


@pytest.mark.skipif(
    not hasattr(importlib, "import_module"),
    reason="importlib.import_module not available",
)
def test_basic_import_module():
    om = objects.ObjectManager()
    with ImportLibImportHook(graph.Graph(), om):
        this = importlib.import_module("this")

    assert om.lookup_module("this") == objects.Module.from_imported(this)


@pytest.mark.skipif(
    not hasattr(importlib, "import_module"),
    reason="importlib.import_module not available",
)
def test_nested_importlib():
    om = objects.ObjectManager()
    with ImportLibImportHook(graph.Graph(), om):
        _message = importlib.import_module("email.mime.message")

    import email.mime.message

    assert om.lookup_module("email") == objects.Module.from_imported(email)
    assert om.lookup_module("email.mime") == objects.Module.from_imported(email.mime)
    assert om.lookup_module("email.mime.message") == objects.Module.from_imported(
        email.mime.message
    )


@pytest.mark.skipif(
    not hasattr(importlib, "import_module"),
    reason="importlib.import_module not available",
)
def test_relative_importlib():
    om = objects.ObjectManager()
    with ImportLibImportHook(graph.Graph(), om):
        _image = importlib.import_module("..message", "email.mime.image")

    import email.mime.message

    assert om.lookup_module("email") == objects.Module.from_imported(email)
    assert om.lookup_module("email.mime") == objects.Module.from_imported(email.mime)
    assert om.lookup_module("email.mime.message") == objects.Module.from_imported(
        email.mime.message
    )
