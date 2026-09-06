"""Recognize basic hand gestures for PowerPoint slide control."""

from __future__ import annotations

import cv2
import mediapipe as mp


class GesturePresentationController:
    """Capture webcam frames and map simple gestures to slide actions."""

    def __init__(self, camera_index: int = 0) -> None:
        self.camera_index = camera_index
        self.camera = cv2.VideoCapture(camera_index)
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        self.drawer = mp.solutions.drawing_utils

    def recognize_gesture(self, landmarks) -> str:
        """Return a starter gesture name from hand landmark positions."""
        if landmarks is None:
            return "unknown"

        # This beginner-friendly heuristic counts raised fingertips.
        fingertip_ids = (8, 12, 16, 20)
        raised_fingers = sum(
            landmarks.landmark[tip].y < landmarks.landmark[tip - 2].y
            for tip in fingertip_ids
        )
        if raised_fingers == 4:
            return "next"
        if raised_fingers == 0:
            return "previous"
        if raised_fingers == 1:
            return "start"
        if raised_fingers == 2:
            return "end"
        return "unknown"

    def execute_action(self, action: str) -> None:
        """Print the selected action; connect this to PowerPoint automation later."""
        print(f"Presentation action: {action}")

    def run(self) -> None:
        """Read webcam frames until the user presses Q."""
        if not self.camera.isOpened():
            raise RuntimeError("Could not open the webcam.")

        while True:
            success, frame = self.camera.read()
            if not success:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                action = self.recognize_gesture(hand_landmarks)
                if action != "unknown":
                    self.execute_action(action)
                self.drawer.draw_landmarks(
                    frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS
                )

            cv2.imshow("Gesture Presentation Control", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.close()

    def close(self) -> None:
        """Release camera and MediaPipe resources."""
        self.camera.release()
        cv2.destroyAllWindows()
        self.hands.close()


if __name__ == "__main__":
    GesturePresentationController().run()
