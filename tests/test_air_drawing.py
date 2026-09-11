"""Tests for the gesture-only air-drawing control scheme."""

import numpy as np

from air_drawing.air_drawing import AirCanvas


def test_gesture_to_action_matches_all_modes():
    assert AirCanvas.gesture_to_action([0, 1, 0, 0, 0]) == "draw"
    assert AirCanvas.gesture_to_action([0, 1, 1, 0, 0]) == "cycle_color"
    assert AirCanvas.gesture_to_action([0, 1, 1, 1, 0]) == "eraser_select"
    assert AirCanvas.gesture_to_action([0, 1, 1, 1, 1]) == "increase_brush_size"
    assert AirCanvas.gesture_to_action([1, 1, 1, 1, 1]) == "clear_all"
    assert AirCanvas.gesture_to_action([0, 0, 0, 0, 0]) == "idle"


def test_debounce_prevents_repeat_actions_for_same_gesture_hold():
    canvas = AirCanvas.__new__(AirCanvas)
    canvas.current_tool = "pencil"
    canvas.current_color = AirCanvas.COLOR_SEQUENCE[0]
    canvas.color_index = 0
    canvas.brush_thickness = 8
    canvas.canvas = np.zeros((10, 10, 3), dtype=np.uint8)
    canvas.last_held_gesture = None

    canvas.handle_discrete_action("cycle_color")
    assert canvas.current_color == AirCanvas.COLOR_SEQUENCE[1]
    assert canvas.current_tool == "pencil"

    canvas.handle_discrete_action("cycle_color")
    assert canvas.current_color == AirCanvas.COLOR_SEQUENCE[1]

    canvas.handle_discrete_action("eraser_select")
    assert canvas.current_tool == "eraser"

    canvas.handle_discrete_action("eraser_select")
    assert canvas.current_tool == "eraser"

    canvas.handle_discrete_action("increase_brush_size")
    assert canvas.brush_thickness == AirCanvas.MIN_BRUSH_THICKNESS

    canvas.handle_discrete_action("increase_brush_size")
    assert canvas.brush_thickness == AirCanvas.MIN_BRUSH_THICKNESS

    canvas.handle_discrete_action("clear_all")
    assert canvas.canvas.size > 0


def test_color_cycle_wraps_around_correctly():
    canvas = AirCanvas.__new__(AirCanvas)
    canvas.color_index = len(AirCanvas.COLOR_SEQUENCE) - 1
    canvas.current_color = AirCanvas.COLOR_SEQUENCE[-1]
    canvas.current_tool = "pencil"

    canvas.cycle_color()

    assert canvas.current_color == AirCanvas.COLOR_SEQUENCE[0]
    assert canvas.current_tool == "pencil"


def test_two_finger_gesture_resets_tool_to_pencil():
    canvas = AirCanvas.__new__(AirCanvas)
    canvas.current_tool = "eraser"
    canvas.current_color = (0, 0, 0)
    canvas.color_index = 0

    canvas.cycle_color()

    assert canvas.current_tool == "pencil"
    assert canvas.current_color == AirCanvas.COLOR_SEQUENCE[1]


def test_smoothing_and_jump_rejection_still_work():
    previous = (100, 100)
    new_point = (200, 200)
    smoothed = AirCanvas.smooth_point(previous, new_point, smoothing_factor=0.5)
    assert smoothed != new_point
    assert smoothed == (150, 150)

    large_jump = (300, 100)
    assert AirCanvas.should_draw_segment(previous, large_jump, max_jump=100) is False


def test_four_finger_gesture_wraps_brush_size_back_to_smallest():
    canvas = AirCanvas.__new__(AirCanvas)
    canvas.brush_thickness = AirCanvas.MAX_BRUSH_THICKNESS
    canvas.last_held_gesture = None

    canvas.increase_brush_size()

    assert canvas.brush_thickness == AirCanvas.MIN_BRUSH_THICKNESS
