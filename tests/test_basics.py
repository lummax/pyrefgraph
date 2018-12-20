# coding=utf-8

import pytest
from tests import utils


@utils.isolated
def test_api():
    import reference_graph

    graph = reference_graph.Graph()
    reference_graph.Analysis()
    reference_graph.Analysis(graph)


@utils.isolated
def test_api_infect():
    import reference_graph

    reference_graph.infect()


@utils.isolated
def test_api_infect_import():
    import reference_graph.infection


@utils.isolated
def test_config_main():
    import argparse
    import reference_graph.config

    ns = argparse.Namespace()
    ns.entry = "invalid"

    with pytest.raises(ImportError):
        reference_graph.config.main(ns)
