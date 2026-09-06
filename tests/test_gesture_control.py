"""Tests for gesture presentation control."""

import pytest

pytest.importorskip("mediapipe")

from gesture_control.gesture_control import GesturePresentationController


def test_gesture_controller_exposes_expected_api():
    assert hasattr(GesturePresentationController, "recognize_gesture")
