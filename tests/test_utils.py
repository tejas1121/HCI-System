"""Tests for shared utilities."""

from utils.helpers import load_config


def test_load_config_returns_empty_dict_for_missing_file(tmp_path):
    assert load_config(tmp_path / "missing.json") == {}
