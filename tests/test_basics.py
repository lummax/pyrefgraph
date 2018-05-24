# coding=utf-8
import argparse
import pytest


def test_api():
    import reference_graph.api
    reference_graph.api.run()


def test_api_infect():
    import reference_graph.api.infect


def test_config_main():
    import reference_graph.config
    with pytest.raises(SystemExit):
        reference_graph.config.main()
