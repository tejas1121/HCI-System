"""Capture speech and map recognized phrases to application commands."""

from __future__ import annotations

from collections.abc import Callable

import speech_recognition as sr


class VoiceAssistant:
    """Convert microphone input into a small set of known commands."""

    def __init__(self) -> None:
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.commands: dict[str, Callable[[], None]] = {
            "next slide": lambda: print("Command: next slide"),
            "previous slide": lambda: print("Command: previous slide"),
            "read slide": lambda: print("Command: read slide"),
            "open file": lambda: print("Command: open file"),
        }

    def parse_command(self, text: str) -> str | None:
        """Return the first known command contained in recognized text."""
        normalized_text = text.lower().strip()
        return next(
            (command for command in self.commands if command in normalized_text),
            None,
        )

    def listen_once(self) -> str | None:
        """Listen once and return recognized English text, if available."""
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"Heard: {text}")
            return text
        except (sr.UnknownValueError, sr.RequestError) as error:
            print(f"Speech recognition unavailable: {error}")
            return None

    def run_once(self) -> str | None:
        """Listen for one command and execute it when recognized."""
        text = self.listen_once()
        if text is None:
            return None
        command = self.parse_command(text)
        if command is None:
            print("Command not recognized.")
            return None
        self.commands[command]()
        return command


if __name__ == "__main__":
    VoiceAssistant().run_once()
