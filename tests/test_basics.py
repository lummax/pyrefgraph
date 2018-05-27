# coding=utf-8
import argparse
import pytest


def test_api():
    import reference_graph

    graph = reference_graph.Graph()
    reference_graph.Analysis()
    reference_graph.Analysis(graph)


def test_api_infect():
    import reference_graph

    reference_graph.infect()


def test_api_infect_import():
    import reference_graph.infection


def test_config_main():
    import reference_graph.config

    with pytest.raises(SystemExit):
        reference_graph.config.main()
