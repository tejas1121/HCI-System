"""Tests for air drawing."""

import pytest

pytest.importorskip("mediapipe")

from air_drawing.air_drawing import AirDrawing


def test_air_drawing_exposes_expected_api():
    assert hasattr(AirDrawing, "clear_canvas")
