"""Application entry point for the multimodal interaction system."""

from __future__ import annotations

from air_drawing import AirDrawing
from desktop_control import DesktopController
from gesture_control import GesturePresentationController
from text_to_speech import SlideReader
from voice_assistant import VoiceAssistant


def show_menu() -> str:
    """Display the starter menu and return the selected option."""
    print("\nMultimodal Interaction System")
    print("1. Gesture presentation control")
    print("2. Air drawing")
    print("3. Voice assistant")
    print("4. Read a PowerPoint presentation")
    print("5. Desktop control demo")
    print("0. Exit")
    return input("Choose an option: ").strip()


def run() -> None:
    """Launch one selected module, then return to the menu."""
    while True:
        choice = show_menu()
        if choice == "1":
            GesturePresentationController().run()
        elif choice == "2":
            AirDrawing().run()
        elif choice == "3":
            VoiceAssistant().run_once()
        elif choice == "4":
            presentation_path = input("Enter the .pptx path: ").strip()
            SlideReader().read_presentation(presentation_path)
        elif choice == "5":
            DesktopController().execute_gesture("scroll_up")
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Please choose a valid option.")


if __name__ == "__main__":
    run()
