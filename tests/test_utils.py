"""Tests for shared utilities."""

from utils.helpers import load_config


def test_load_config_returns_defaults_for_missing_file(tmp_path):
    assert load_config(str(tmp_path / "missing.json")) == {
        "camera_index": 0,
        "detection_confidence": 0.7,
        "tracking_confidence": 0.7,
    }
