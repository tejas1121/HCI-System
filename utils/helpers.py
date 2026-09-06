"""Shared camera, logging, and configuration helpers."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import cv2


def create_camera(camera_index: int = 0) -> cv2.VideoCapture:
    """Create and return an OpenCV webcam capture object."""
    return cv2.VideoCapture(camera_index)


def get_logger(name: str = "multimodal_system") -> logging.Logger:
    """Return a consistently configured project logger."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    return logging.getLogger(name)


def load_config(config_path: str | Path = "config.json") -> dict:
    """Load JSON configuration, returning an empty dict when absent."""
    path = Path(config_path)
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as config_file:
        return json.load(config_file)


if __name__ == "__main__":
    print(load_config())
