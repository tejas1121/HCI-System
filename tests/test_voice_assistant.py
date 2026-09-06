"""Tests for voice command parsing."""

import pytest

pytest.importorskip("speech_recognition")

from voice_assistant.voice_assistant import VoiceAssistant


def test_voice_command_parser_matches_known_phrase():
    assistant = VoiceAssistant.__new__(VoiceAssistant)
    assistant.commands = {"next slide": lambda: None}
    assert assistant.parse_command("Please go to the next slide") == "next slide"
