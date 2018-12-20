# coding=utf-8
import os
import glob
import pytest
import itertools
import subprocess


BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SOURCE_PATHS = (
    os.path.join(BASE_PATH, "reference_graph"),
    os.path.join(BASE_PATH, "examples"),
)
ALL_SOURCE_PATHS = SOURCE_PATHS + (os.path.join(BASE_PATH, "tests"),)
SOURCE_FILES = tuple(
    itertools.chain.from_iterable(
        glob.iglob(os.path.join(p, "*.py")) for p in ALL_SOURCE_PATHS
    )
)


def is_available(*args):
    try:
        subprocess.check_call(args)
    except (EnvironmentError, subprocess.CalledProcessError):
        return False
    return True


def run_tool(args, check_stdout=True, check_stderr=True):
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = process.communicate()
    assert not check_stdout or not stdout
    assert not check_stderr or not stderr
    assert process.returncode == 0


@pytest.mark.slow
@pytest.mark.skipif(
    not is_available("black", "--version"), reason="black is not installed"
)
@pytest.mark.parametrize("path", SOURCE_FILES)
def test_black(path):
    return run_tool(("black", "--check", "--quiet", path))


@pytest.mark.slow
@pytest.mark.skipif(
    not is_available("mypy", "--version"), reason="mypy is not installed"
)
@pytest.mark.parametrize("path", SOURCE_PATHS)
def test_mypy(path):
    return run_tool(("mypy", path))


@pytest.mark.slow
def test_pyrefgraph():
    return run_tool(("pyrefgraph", "--help"), check_stdout=False)
