"""Shared camera, logging, and configuration helpers."""

import json
import logging
import os

import cv2


DEFAULT_CONFIG = {
    "camera_index": 0,
    "detection_confidence": 0.7,
    "tracking_confidence": 0.7,
}


def get_camera(index: int = 0) -> cv2.VideoCapture:
    """Open and return the webcam at ``index`` or raise a clear error."""
    camera = cv2.VideoCapture(index)
    if not camera.isOpened():
        camera.release()
        raise RuntimeError(
            f"Unable to open camera {index}; check that it is connected "
            "and not already in use."
        )
    return camera


def setup_logger(name: str) -> logging.Logger:
    """Return a console logger with timestamped, leveled messages."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not any(getattr(handler, "_helpers_handler", False) for handler in logger.handlers):
        handler = logging.StreamHandler()
        handler._helpers_handler = True
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        logger.addHandler(handler)
    return logger


def load_config(path: str = "config.json") -> dict:
    """Load a JSON config merged over the project defaults."""
    config = DEFAULT_CONFIG.copy()
    try:
        with open(os.fspath(path), encoding="utf-8") as config_file:
            loaded_config = json.load(config_file)
    except (OSError, json.JSONDecodeError, TypeError):
        return config

    if isinstance(loaded_config, dict):
        config.update(loaded_config)
    return config


def create_camera(camera_index: int = 0) -> cv2.VideoCapture:
    """Compatibility wrapper for :func:`get_camera`."""
    return get_camera(camera_index)


def get_logger(name: str = "multimodal_system") -> logging.Logger:
    """Compatibility wrapper for :func:`setup_logger`."""
    return setup_logger(name)
