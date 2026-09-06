"""Draw simple annotations in the air using hand landmarks."""

from __future__ import annotations

import cv2
import mediapipe as mp
import numpy as np


class AirDrawing:
    """Use a webcam hand signal as a virtual pen and eraser."""

    def __init__(self, camera_index: int = 0) -> None:
        self.camera = cv2.VideoCapture(camera_index)
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        self.drawer = mp.solutions.drawing_utils
        self.canvas = None
        self.previous_point = None

    @staticmethod
    def count_raised_fingers(hand_landmarks) -> int:
        """Count raised fingers using the four non-thumb fingertips."""
        fingertip_ids = (8, 12, 16, 20)
        return sum(
            hand_landmarks.landmark[tip].y
            < hand_landmarks.landmark[tip - 2].y
            for tip in fingertip_ids
        )

    def draw_point(self, point: tuple[int, int], eraser: bool = False) -> None:
        """Draw a line segment or erase around the current fingertip."""
        if self.canvas is None:
            return
        color = (0, 0, 0) if eraser else (0, 255, 0)
        thickness = 30 if eraser else 5
        if self.previous_point is not None:
            cv2.line(self.canvas, self.previous_point, point, color, thickness)
        self.previous_point = point

    def clear_canvas(self) -> None:
        """Remove all annotations from the canvas."""
        if self.canvas is not None:
            self.canvas[:] = 0
        self.previous_point = None

    def run(self) -> None:
        """Capture webcam frames until the user presses Q."""
        if not self.camera.isOpened():
            raise RuntimeError("Could not open the webcam.")

        while True:
            success, frame = self.camera.read()
            if not success:
                break
            if self.canvas is None:
                self.canvas = np.zeros_like(frame)

            results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.previous_point = None
            if results.multi_hand_landmarks:
                hand = results.multi_hand_landmarks[0]
                raised = self.count_raised_fingers(hand)
                index = hand.landmark[8]
                point = (int(index.x * frame.shape[1]), int(index.y * frame.shape[0]))

                if raised == 0:
                    self.clear_canvas()
                elif raised == 2:
                    self.draw_point(point, eraser=True)
                elif raised >= 1:
                    self.draw_point(point)
                self.drawer.draw_landmarks(frame, hand, mp.solutions.hands.HAND_CONNECTIONS)

            output = cv2.addWeighted(frame, 0.7, self.canvas, 0.3, 0)
            cv2.imshow("Air Drawing", output)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.close()

    def close(self) -> None:
        """Release camera and MediaPipe resources."""
        self.camera.release()
        cv2.destroyAllWindows()
        self.hands.close()


if __name__ == "__main__":
    AirDrawing().run()
