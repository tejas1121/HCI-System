# AI-Powered Multimodal Presentation and Hands-Free Computer Interaction System

> An integrated accessibility platform that combines hand gestures, voice assistance, air drawing, text-to-speech, and desktop control for natural, hands-free computer interaction.

## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Research Gap](#research-gap)
- [Key Features and Modules](#key-features-and-modules)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Contribution Guidelines](#contribution-guidelines)
- [License](#license)
- [Contributors](#contributors)

## Overview

Traditional presentation and desktop systems depend on a keyboard, mouse, or handheld remote. These interaction methods can be inconvenient for hands-free presenters and create additional barriers for visually impaired users.

This project develops a unified multimodal interaction system that enables users to control presentations and selected desktop functions through hand gestures and voice commands. It combines computer vision, speech processing, OCR, text-to-speech, and PowerPoint automation in a single accessibility-focused platform.

The project belongs to the following domains:

- Artificial Intelligence and Machine Learning
- Computer Vision
- Human-Computer Interaction
- Accessibility Technology

## Problem Statement

Existing presentation and accessibility tools often have separate, limited capabilities. Key challenges include:

- Dependence on keyboards, mice, and physical remotes
- Limited gesture functionality in existing presentation tools
- Voice assistants and accessibility features operating independently
- Lack of unified hands-free desktop interaction
- Insufficient support for visually impaired users during presentations

## Research Gap

Very few systems integrate gesture recognition, voice commands, air drawing, text-to-speech, and desktop control into one intelligent accessibility platform. This project addresses that gap by combining these capabilities into a single multimodal interaction system.

## Key Features and Modules

### 1. Hand Gesture Presentation Control

Controls PowerPoint presentations using real-time hand gestures. OpenCV and MediaPipe detect 21 hand landmarks, which are interpreted as presentation actions such as navigating between slides.

### 2. Air Drawing and Annotation

Allows users to draw or annotate on the screen without touching a physical input device.

- Two fingers: activate drawing mode
- Index finger: act as a virtual pen
- Fist: clear the canvas
- Two fingers together: activate the eraser

### 3. Voice Command Processing

Captures speech through a microphone, converts it to text, interprets the command, and executes the requested presentation or desktop action.

### 4. Text-to-Speech Slide Reading

Extracts text from the current slide and reads it aloud to support visually impaired users. OCR is used as a fallback when text is embedded inside images or cannot be extracted directly.

### 5. Gesture-Based Desktop Control

Uses recognized hand gestures to control selected operating-system functions, reducing the need for a keyboard or mouse during supported workflows.

## Technology Stack

| Area | Technologies |
| --- | --- |
| Programming language | Python |
| Computer vision | OpenCV, MediaPipe |
| Hand tracking | MediaPipe Hands, 21 hand landmarks |
| Speech recognition | Python speech-recognition tooling and microphone input |
| Text-to-speech | Python-compatible TTS engine |
| OCR | OCR engine for text inside slide images |
| Presentation automation | PowerPoint automation libraries |
| Collaboration | Git and GitHub |
| Testing | Python unit testing tools |

## Project Structure

```text
project-root/
├── gesture_control/
│   ├── __init__.py
│   └── gesture_control.py  # Module 1: Presentation control via gestures
├── air_drawing/
│   ├── __init__.py
│   └── air_drawing.py      # Module 2: Air drawing and annotation
├── voice_assistant/
│   ├── __init__.py
│   └── voice_assistant.py  # Module 3: Voice command processing
├── text_to_speech/
│   ├── __init__.py
│   └── text_to_speech.py   # Module 4: TTS slide reading and OCR
├── desktop_control/
│   ├── __init__.py
│   └── desktop_control.py  # Module 5: Gesture-based desktop control
├── utils/
│   ├── __init__.py
│   └── helpers.py          # Shared camera, logging, and config helpers
├── assets/                 # Images, icons, and sample media
├── docs/                   # Additional project documentation
├── tests/
│   ├── __init__.py
│   └── test_<module>.py    # Basic tests for each module
├── requirements.txt        # Python dependencies
├── main.py                 # Application entry point
├── .gitignore
└── README.md               # Project documentation
```

## Installation and Setup

### Prerequisites

- Python 3.9 or later
- A webcam
- A microphone for voice commands
- PowerPoint, if presentation automation is enabled
- An OCR engine configured according to the project implementation

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/<organization-or-username>/<repository-name>.git
   cd <repository-name>
   ```

2. Create and activate a virtual environment.

   **Windows PowerShell:**

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   **macOS/Linux:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install the project dependencies:

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Connect the webcam and microphone, open a supported presentation if required, and start the application:

   ```bash
   python main.py
   ```

5. Run the starter test suite:

   ```bash
   python -m pytest
   ```

> PowerPoint automation and some desktop-control features may depend on the operating system and installed applications. Configure any required OCR, audio, or PowerPoint settings before running the system.

## Usage

After starting the application, use the webcam and microphone to interact with the system.

### Example gestures

- Open hand or configured next-slide gesture: move to the next slide
- Configured previous-slide gesture: return to the previous slide
- Two fingers: enter air-drawing mode
- Index finger: draw or annotate on the screen
- Fist: clear the current annotation canvas
- Two fingers together: erase annotations

The exact gesture mappings are defined by the implementation in `gesture_control/` and `desktop_control/`.

### Example voice commands

Depending on the configured command set, users may say commands such as:

```text
"Next slide"
"Previous slide"
"Read this slide"
"Start drawing"
"Clear annotations"
"Exit presentation"
```

Use a quiet environment and speak clearly for more reliable speech recognition. The application should be tested with the intended microphone, camera, presentation format, and operating system.

## Contribution Guidelines

This is a team project with **4 contributors** collaborating through GitHub.

- Never push directly to the `main` branch.
- Always create a new branch for each feature or fix. For example:
  - `feature/gesture-control`
  - `fix/voice-bug`
  - `docs/readme-update`
- Open a Pull Request to merge changes into `main`.
- At least one other team member must review and approve the Pull Request before it is merged.
- Keep commits small, focused, and descriptive.
- Pull the latest `main` branch and rebase or merge it into your working branch before starting new work to reduce conflicts.
- Add or update tests when changing module behavior.
- Document new commands, configuration, or dependencies in the README and project files.

A typical workflow is:

```bash
git checkout main
git pull origin main
git checkout -b feature/your-feature

# Make and test changes
git add .
git commit -m "Add descriptive change"
git push -u origin feature/your-feature
```

Then open a Pull Request on GitHub and request review from at least one team member.

## License

This project is licensed under the [MIT License](https://opensource.org/license/mit/).

Add the complete MIT license text to a `LICENSE` file before distributing the project.

## Contributors

This project is developed by a team of four contributors:

1. **[Team Member 1]** - Project lead / integration
2. **[Team Member 2]** - Gesture recognition and computer vision
3. **[Team Member 3]** - Voice assistance and text-to-speech
4. **[Team Member 4]** - Testing, documentation, and desktop control

Replace the placeholder names and role descriptions with the team members' actual details.
