"""Provide simple gesture-triggered desktop actions."""

from __future__ import annotations

import pyautogui


class DesktopController:
    """Wrap selected pyautogui operations behind readable methods."""

    def move_mouse(self, x: int, y: int) -> None:
        """Move the pointer to a screen coordinate."""
        pyautogui.moveTo(x, y, duration=0.1)

    def scroll(self, amount: int) -> None:
        """Scroll up or down using a signed amount."""
        pyautogui.scroll(amount)

    def volume_up(self) -> None:
        """Press the system volume-up key."""
        pyautogui.press("volumeup")

    def volume_down(self) -> None:
        """Press the system volume-down key."""
        pyautogui.press("volumedown")

    def execute_gesture(self, gesture: str) -> None:
        """Map a starter gesture label to a desktop operation."""
        actions = {
            "volume_up": self.volume_up,
            "volume_down": self.volume_down,
            "scroll_up": lambda: self.scroll(5),
            "scroll_down": lambda: self.scroll(-5),
        }
        action = actions.get(gesture)
        if action is None:
            print(f"Unknown desktop gesture: {gesture}")
            return
        action()


if __name__ == "__main__":
    print("Desktop control demo: scrolling up five steps.")
    DesktopController().scroll(5)
