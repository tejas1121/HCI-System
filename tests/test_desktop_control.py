"""Tests for desktop control."""

import pytest

pytest.importorskip("pyautogui")

from desktop_control.desktop_control import DesktopController


def test_desktop_controller_exposes_gesture_dispatch():
    assert hasattr(DesktopController, "execute_gesture")
