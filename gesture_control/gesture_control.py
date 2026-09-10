"""Recognize basic hand gestures for PowerPoint slide control."""

from __future__ import annotations

import time

import cv2

from utils.hand_tracking import HandTracker
from utils.helpers import get_camera, setup_logger


class GestureController:
    """Capture webcam frames and map simple gestures to slide actions."""

    COOLDOWN_SECONDS = 1.5

    def __init__(self) -> None:
        self.tracker = HandTracker()
        self.camera = get_camera()
        self.logger = setup_logger(__name__)
        self.last_action_time = 0.0

    @staticmethod
    def gesture_to_action(pattern: list[int] | tuple[int, ...]) -> str | None:
        """Map a finger pattern to a presentation action."""
        actions = {
            (0, 1, 0, 0, 0): "next slide",
            (0, 1, 1, 0, 0): "previous slide",
            (1, 1, 1, 1, 1): "start presentation",
            (0, 0, 0, 0, 0): "end presentation",
        }
        return actions.get(tuple(pattern))

    recognize_gesture = gesture_to_action

    def _trigger_pptx_action(self, action: str) -> None:
        """Print the selected action; connect this to PowerPoint automation later."""
        self.logger.info("Presentation action: %s", action)

    def run(self) -> None:
        """Read webcam frames until the user presses Q."""
        try:
            while True:
                success, frame = self.camera.read()
                if not success:
                    break
                hands = self.tracker.find_hands(frame)
                if hands:
                    pattern = self.tracker.fingers_up(hands[0])
                    action = self.gesture_to_action(pattern)
                    now = time.monotonic()
                    if action and now - self.last_action_time >= self.COOLDOWN_SECONDS:
                        self.last_action_time = now
                        self.logger.info("Gesture action: %s", action)
                        self._trigger_pptx_action(action)
                cv2.imshow("Gesture Presentation Control", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            self.close()

    def close(self) -> None:
        """Release camera and MediaPipe resources."""
        self.camera.release()
        cv2.destroyAllWindows()
        self.tracker.shutdown()


GesturePresentationController = GestureController


if __name__ == "__main__":
    GestureController().run()
