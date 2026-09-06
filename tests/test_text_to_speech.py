"""Tests for slide text extraction."""

import pytest

pytest.importorskip("pyttsx3")
pytest.importorskip("pytesseract")
pytest.importorskip("pptx")

from text_to_speech.text_to_speech import SlideReader


def test_slide_reader_exposes_text_extraction():
    assert hasattr(SlideReader, "extract_text_from_slide")
