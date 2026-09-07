"""Tests for shared helper functions."""

import json

from utils.helpers import load_config, setup_logger


DEFAULT_CONFIG = {
    "camera_index": 0,
    "detection_confidence": 0.7,
    "tracking_confidence": 0.7,
}


def test_load_config_returns_defaults_when_file_does_not_exist(tmp_path):
    assert load_config(str(tmp_path / "missing.json")) == DEFAULT_CONFIG


def test_load_config_merges_partial_config(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"camera_index": 1}), encoding="utf-8")

    assert load_config(str(config_path)) == {
        "camera_index": 1,
        "detection_confidence": 0.7,
        "tracking_confidence": 0.7,
    }


def test_load_config_returns_defaults_for_invalid_json(tmp_path):
    config_path = tmp_path / "config.json"
    config_path.write_text("{invalid", encoding="utf-8")

    assert load_config(str(config_path)) == DEFAULT_CONFIG


def test_setup_logger_reuses_handlers():
    logger_name = "tests.helpers"
    first_logger = setup_logger(logger_name)
    initial_handler_count = len(first_logger.handlers)

    second_logger = setup_logger(logger_name)

    assert second_logger is first_logger
    assert second_logger.name == logger_name
    assert len(second_logger.handlers) == initial_handler_count
    assert initial_handler_count == 1