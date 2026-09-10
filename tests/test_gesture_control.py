"""Tests for gesture-to-presentation-action mapping."""

from gesture_control.gesture_control import GestureController


def test_index_finger_maps_to_next_slide():
    assert GestureController.gesture_to_action([0, 1, 0, 0, 0]) == "next slide"


def test_index_and_middle_map_to_previous_slide():
    assert GestureController.gesture_to_action([0, 1, 1, 0, 0]) == "previous slide"


def test_open_palm_maps_to_start():
    assert GestureController.gesture_to_action([1, 1, 1, 1, 1]) == "start presentation"


def test_fist_maps_to_end():
    assert GestureController.gesture_to_action([0, 0, 0, 0, 0]) == "end presentation"
