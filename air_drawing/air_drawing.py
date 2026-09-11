"""Air-drawing controller using a simple gesture-based control scheme."""

from __future__ import annotations

import cv2
import numpy as np

from utils.hand_tracking import HandTracker
from utils.helpers import get_camera, setup_logger


class AirCanvas:
    """Use hand gestures to draw, change color, erase, or clear the canvas."""

    COLOR_SEQUENCE = [
        (0, 0, 255),
        (0, 255, 0),
        (255, 0, 0),
        (0, 255, 255),
    ]
    COLOR_NAMES = ["Red", "Green", "Blue", "Yellow"]
    DEFAULT_BRUSH_THICKNESS = 8
    MIN_BRUSH_THICKNESS = 2
    MAX_BRUSH_THICKNESS = 40

    def __init__(self) -> None:
        self.tracker = HandTracker()
        self.camera = get_camera()
        self.logger = setup_logger(__name__)
        success, frame = self.camera.read()
        if not success:
            self.camera.release()
            raise RuntimeError("Unable to read an initial frame from the camera.")

        self.canvas = np.zeros_like(frame)
        self.current_tool = "pencil"
        self.current_color = self.COLOR_SEQUENCE[0]
        self.color_index = 0
        self.brush_thickness = self.DEFAULT_BRUSH_THICKNESS
        self.prev_point = None
        self.smoothing_factor = 0.6
        self.max_jump_distance = 100
        self.last_held_gesture = None

    @staticmethod
    def gesture_to_action(pattern: list[int] | tuple[int, ...]) -> str:
        """Map a finger pattern to a simple discrete action."""
        one_finger = (0, 1, 0, 0, 0)
        two_fingers = (0, 1, 1, 0, 0)
        three_fingers = (0, 1, 1, 1, 0)
        four_fingers = (0, 1, 1, 1, 1)
        open_palm = (1, 1, 1, 1, 1)

        actions = {
            one_finger: "draw",
            two_fingers: "cycle_color",
            three_fingers: "eraser_select",
            four_fingers: "increase_brush_size",
            open_palm: "clear_all",
        }
        return actions.get(tuple(pattern), "idle")

    @property
    def previous_point(self):
        return self.prev_point

    @staticmethod
    def smooth_point(
        previous_point: tuple[int, int] | None,
        new_point: tuple[int, int],
        smoothing_factor: float = 0.6,
    ) -> tuple[int, int]:
        """Apply exponential smoothing to reduce jitter in the drawn path."""
        if previous_point is None:
            return new_point
        prev_x, prev_y = previous_point
        new_x, new_y = new_point
        smoothed_x = prev_x + (new_x - prev_x) * smoothing_factor
        smoothed_y = prev_y + (new_y - prev_y) * smoothing_factor
        return int(smoothed_x), int(smoothed_y)

    @staticmethod
    def should_draw_segment(
        previous_point: tuple[int, int] | None,
        new_point: tuple[int, int] | None,
        max_jump: int = 100,
    ) -> bool:
        """Reject unexpected large jumps from noisy tracking data."""
        if previous_point is None or new_point is None:
            return True
        distance = np.hypot(
            new_point[0] - previous_point[0],
            new_point[1] - previous_point[1],
        )
        return bool(distance <= max_jump)

    def cycle_color(self) -> None:
        """Move to the next color in the fixed sequence and restore pencil mode."""
        self.color_index = (self.color_index + 1) % len(self.COLOR_SEQUENCE)
        self.current_color = self.COLOR_SEQUENCE[self.color_index]
        self.current_tool = "pencil"

    def select_eraser(self) -> None:
        """Switch the active tool to eraser without erasing immediately."""
        self.current_tool = "eraser"
        self.brush_thickness = max(self.brush_thickness, 40)

    def clear_canvas(self) -> None:
        """Erase the entire canvas."""
        self.canvas[:] = 0
        self.prev_point = None

    def draw_point(self, point: tuple[int, int]) -> None:
        """Draw a line segment with the active tool and thickness."""
        if self.prev_point is None:
            self.prev_point = point
            return

        if not self.should_draw_segment(self.prev_point, point, self.max_jump_distance):
            self.prev_point = point
            return

        color = self.current_color if self.current_tool == "pencil" else (0, 0, 0)
        cv2.line(self.canvas, self.prev_point, point, color, self.brush_thickness)
        self.prev_point = point

    def increase_brush_size(self) -> None:
        """Increase brush thickness, wrapping back to the minimum when the max is reached."""
        if self.brush_thickness >= self.MAX_BRUSH_THICKNESS:
            self.brush_thickness = self.MIN_BRUSH_THICKNESS
        else:
            self.brush_thickness = min(self.brush_thickness + 2, self.MAX_BRUSH_THICKNESS)

    def handle_discrete_action(self, gesture: str) -> None:
        """Process a discrete action only once per gesture hold."""
        if gesture == "cycle_color" and self.last_held_gesture != gesture:
            self.cycle_color()
            self.last_held_gesture = gesture
        elif gesture == "eraser_select" and self.last_held_gesture != gesture:
            self.select_eraser()
            self.last_held_gesture = gesture
        elif gesture == "increase_brush_size" and self.last_held_gesture != gesture:
            self.increase_brush_size()
            self.last_held_gesture = gesture
        elif gesture == "clear_all" and self.last_held_gesture != gesture:
            self.clear_canvas()
            self.last_held_gesture = gesture
        elif gesture != "draw" and gesture != "idle":
            self.last_held_gesture = gesture

    def draw_overlay(self, frame) -> None:
        """Display the active tool, color, and brush thickness on the video."""
        color_name = self.COLOR_NAMES[self.color_index]
        tool_label = "Eraser" if self.current_tool == "eraser" else "Pencil"
        text_lines = [
            f"Tool: {tool_label}",
            f"Color: {color_name if self.current_tool == 'pencil' else 'Black'}",
            f"Brush: {self.brush_thickness}",
        ]
        for index, line in enumerate(text_lines):
            cv2.putText(
                frame,
                line,
                (10, 30 + index * 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )

    def run(self) -> None:
        """Read webcam frames until the user presses Q."""
        try:
            while True:
                success, frame = self.camera.read()
                if not success:
                    break

                hands = self.tracker.find_hands(frame)
                if hands:
                    hand = hands[0]
                    fingers = self.tracker.fingers_up(hand)
                    pattern = tuple(fingers)
                    gesture = self.gesture_to_action(pattern)

                    if hasattr(self.tracker, "get_landmark_positions"):
                        landmarks = self.tracker.get_landmark_positions(hand)
                    else:
                        landmarks = [(lm.x, lm.y, lm.z) for lm in hand.landmark]

                    index_tip = landmarks[8]
                    point = (int(index_tip[0] * frame.shape[1]), int(index_tip[1] * frame.shape[0]))

                    if gesture == "draw":
                        smoothed = self.smooth_point(self.prev_point, point, self.smoothing_factor)
                        if self.should_draw_segment(self.prev_point, smoothed, self.max_jump_distance):
                            self.draw_point(smoothed)
                        else:
                            self.prev_point = smoothed
                        self.last_held_gesture = "draw"
                    elif gesture in {"cycle_color", "eraser_select", "increase_brush_size", "clear_all"}:
                        self.handle_discrete_action(gesture)
                    else:
                        self.prev_point = None
                        self.last_held_gesture = "idle"
                else:
                    self.prev_point = None
                    self.last_held_gesture = None

                output = cv2.addWeighted(frame, 0.7, self.canvas, 0.3, 0)
                self.draw_overlay(output)
                cv2.imshow("Air Drawing", output)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break
                if key == ord("+"):
                    self.brush_thickness = min(self.brush_thickness + 2, 40)
                elif key == ord("-"):
                    self.brush_thickness = max(self.brush_thickness - 2, 2)
                elif key == ord("c"):
                    self.clear_canvas()
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
