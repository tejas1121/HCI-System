"""Draw simple annotations in the air using hand landmarks."""

from __future__ import annotations

import cv2
import numpy as np

from utils.hand_tracking import HandTracker
from utils.helpers import get_camera, setup_logger


class AirCanvas:
    """Use a webcam hand signal as a virtual pen and eraser."""

    def __init__(self) -> None:
        self.tracker = HandTracker()
        self.camera = get_camera()
        self.logger = setup_logger(__name__)
        success, frame = self.camera.read()
        if not success:
            self.camera.release()
            raise RuntimeError("Unable to read an initial frame from the camera.")
        self.canvas = np.zeros_like(frame)
        self.xp, self.yp = None, None

    @staticmethod
    def gesture_to_mode(pattern: list[int] | tuple[int, ...]) -> str | None:
        """Map a finger pattern to a drawing mode."""
        modes = {
            (0, 1, 0, 0, 0): "drawing",
            (0, 1, 1, 0, 0): "selection",
            (0, 0, 0, 0, 0): "clear",
            (1, 0, 0, 0, 1): "eraser",
            (0, 1, 1, 1, 0): "eraser",
        }
        return modes.get(tuple(pattern))

    @property
    def previous_point(self):
        return None if self.xp is None or self.yp is None else (self.xp, self.yp)

    def draw_point(self, point: tuple[int, int], eraser: bool = False) -> None:
        """Draw a line segment or erase around the current fingertip."""
        color = (0, 0, 0) if eraser else (0, 255, 0)
        thickness = 30 if eraser else 5
        if self.previous_point is not None:
            cv2.line(self.canvas, self.previous_point, point, color, thickness)
        self.xp, self.yp = point

    def clear_canvas(self) -> None:
        """Remove all annotations from the canvas."""
        self.canvas[:] = 0
        self.xp, self.yp = None, None

    def run(self) -> None:
        """Capture webcam frames until the user presses Q."""
        try:
            while True:
                success, frame = self.camera.read()
                if not success:
                    break
                hands = self.tracker.find_hands(frame)
                if hands:
                    hand = hands[0]
                    mode = self.gesture_to_mode(self.tracker.fingers_up(hand))
                    index = hand.landmark[8]
                    point = (int(index.x * frame.shape[1]), int(index.y * frame.shape[0]))
                    if mode == "drawing":
                        self.draw_point(point)
                    elif mode == "selection":
                        self.xp, self.yp = point
                    elif mode == "clear":
                        self.clear_canvas()
                    elif mode == "eraser":
                        self.draw_point(point, eraser=True)
                else:
                    self.xp, self.yp = None, None
                output = cv2.addWeighted(frame, 0.7, self.canvas, 0.3, 0)
                cv2.imshow("Air Drawing", output)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
        finally:
            self.close()

    def close(self) -> None:
        """Release camera and MediaPipe resources."""
        self.camera.release()
        cv2.destroyAllWindows()
        self.tracker.shutdown()


AirDrawing = AirCanvas


if __name__ == "__main__":
    AirCanvas().run()
