"""Tests for gesture-to-air-drawing-mode mapping."""

from air_drawing.air_drawing import AirCanvas


def test_index_finger_selects_drawing_mode():
    assert AirCanvas.gesture_to_mode([0, 1, 0, 0, 0]) == "drawing"


def test_index_and_middle_select_selection_mode():
    assert AirCanvas.gesture_to_mode([0, 1, 1, 0, 0]) == "selection"


def test_fist_clears_canvas():
    assert AirCanvas.gesture_to_mode([0, 0, 0, 0, 0]) == "clear"


def test_thumb_and_pinky_select_eraser_mode():
    assert AirCanvas.gesture_to_mode([1, 0, 0, 0, 1]) == "eraser"


def test_three_fingers_select_eraser_mode():
    assert AirCanvas.gesture_to_mode([0, 1, 1, 1, 0]) == "eraser"
