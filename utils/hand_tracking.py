"""Shared MediaPipe hand-tracking wrapper."""

from __future__ import annotations

import cv2


class HandTracker:
    """Find one hand and expose its landmarks and raised-finger pattern."""

    def __init__(self) -> None:
        try:
            import mediapipe as mp
        except ImportError as error:
            raise RuntimeError("MediaPipe is required for hand tracking.") from error

        self._mp = mp
        self._hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )

    def find_hands(self, frame):
        """Return detected hands and draw their landmarks on ``frame``."""
        results = self._hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        hands = results.multi_hand_landmarks or []
        for hand in hands:
            self._mp.solutions.drawing_utils.draw_landmarks(
                frame, hand, self._mp.solutions.hands.HAND_CONNECTIONS
            )
        return hands

    @staticmethod
    def get_landmark_positions(hand_landmarks) -> list[tuple[float, float, float]]:
        """Return a list of normalized landmark coordinates for the current hand."""
        return [
            (landmark.x, landmark.y, landmark.z)
            for landmark in hand_landmarks.landmark
        ]

    @staticmethod
    def fingers_up(hand_landmarks) -> list[int]:
        """Return ``[thumb, index, middle, ring, pinky]`` as 0/1 values."""
        landmarks = hand_landmarks.landmark
        fingers = [int(landmarks[4].x > landmarks[3].x)]
        fingers.extend(
            int(landmarks[tip].y < landmarks[tip - 2].y)
            for tip in (8, 12, 16, 20)
        )
        return fingers

    @staticmethod
    def close() -> None:
        """Close the tracker resources."""
        return None

    def shutdown(self) -> None:
        self._hands.close()
