# Leipov

Leipov is a local voice-enabled AI assistant built in Python.

The application uses push-to-talk voice input, local speech recognition, optional screenshot capture, the OpenAI API, and text-to-speech to create an interactive desktop assistant with a configurable personality.

Leipov does not like the user very much, but he finds most humans pretty alright.

## Features

- Push-to-talk voice recording
- Local speech-to-text using Faster-Whisper
- OpenAI API integration
- Optional screenshot capture for visual context
- Multimodal prompts using voice and image input
- Text-to-speech responses using Edge TTS
- Tkinter desktop interface
- Recent conversation history
- Configurable personality prompt
- Configurable hotkeys
- Configurable model and voice settings
- Local API key storage

## How It Works

The basic interaction flow is:

    Voice Input
        |
        v
    Faster-Whisper
        |
        v
    Transcribed Text
        |
        +-------------------+
        |                   |
        | Optional          |
        v                   v
    Screenshot Capture    Text Prompt
        |                   |
        +---------+---------+
                  |
                  v
             OpenAI API
                  |
                  v
             AI Response
                  |
                  v
              Edge TTS
                  |
                  v
             Voice Output

The application can also maintain recent conversation context so follow-up interactions can reference previous responses.

## Important First Step

This project requires an OpenAI API key.

In the same folder as `leipov.py`, create a file named:

    leipovkey.txt

Inside that file, paste your OpenAI API key by itself:

    sk-your-api-key-goes-here

Do not include extra text, quotes, spaces, or labels.

The API key is loaded locally when the application starts.

## API Key Warning

Never upload your API key to GitHub.

Make sure `.gitignore` includes:

    leipovkey.txt
    venv/
    __pycache__/
    *.pyc
    .env

If an API key is accidentally committed, revoke or rotate it immediately.

## Setup

Clone the repository:

    git clone YOUR_REPO_LINK_HERE
    cd YOUR_REPO_FOLDER_HERE

Create a virtual environment:

    python -m venv venv

Activate it in Git Bash on Windows:

    source venv/Scripts/activate

Install requirements:

    pip install -r requirements.txt

## Running Leipov

Run:

    python leipov.py

The application will open a local Tkinter interface.

Use the configured push-to-talk hotkey to begin recording.

Press the hotkey again to stop recording and process the input.

Leipov will:

1. Transcribe the recorded audio locally.
2. Optionally capture a screenshot for visual context.
3. Send the prompt and optional image to the OpenAI API.
4. Display the response in the interface.
5. Read the response aloud using text-to-speech.

## Configuration

The code is intentionally organized so common settings can be changed without modifying the application's core logic.

Important configuration sections are clearly marked in the source code.

Common settings include:

- OpenAI model
- Personality/system prompt
- Push-to-talk hotkey
- Screenshot hotkey
- Voice selection
- Screenshot settings
- Conversation behavior

This structure is intended to make the project easier to customize even for users with limited programming experience.

## Screenshot Support

Leipov can capture screenshots using MSS and process them with Pillow.

Screenshots can be included with a spoken prompt and sent to a multimodal OpenAI model for additional visual context.

This allows interactions such as asking the assistant about information currently visible on screen.

## Speech Recognition

Voice input is processed locally using Faster-Whisper.

Recording begins when the configured push-to-talk hotkey is activated and ends when the hotkey is activated again.

The resulting transcription is displayed in the interface before being used as part of the AI request.

## Text-to-Speech

Responses are converted to speech using Edge TTS.

The voice can be changed through the configurable settings section in the source code.

## User Interface

The Tkinter interface displays:

- Recording state
- Recognized speech
- AI responses
- Application status

The interface provides a simple way to see what the assistant heard and how it responded while voice interaction is running.

## Conversation Context

Leipov maintains recent conversation history so responses can reference previous interactions instead of treating every prompt as completely independent.

Conversation history is included with OpenAI requests within the application's configured context limits.

## Tech Stack

- Python
- OpenAI API
- Faster-Whisper
- Edge TTS
- Tkinter
- MSS
- Pillow

## Project Goals

Leipov began as an experiment in creating an AI personality that could interact more naturally than a standard text chatbot.

The project evolved into a local voice-enabled assistant that combines:

- Speech recognition
- Large language models
- Multimodal input
- Screenshot analysis
- Text-to-speech
- Desktop UI development
- Prompt engineering
- Local configuration management

The application is structured so its personality and behavior can be changed without rebuilding the underlying interaction pipeline.

## Example Use Cases

- Voice-enabled desktop assistant
- Screenshot-aware AI assistant
- AI character or personality system
- Stream companion
- Accessibility experiments
- Hands-free AI interaction
- Multimodal interface experiments

## Current Status

Leipov is a functional local prototype.

Current functionality includes:

- Push-to-talk recording
- Local speech recognition
- OpenAI responses
- Screenshot input
- Multimodal prompts
- Text-to-speech output
- Conversation history
- Tkinter interface
- Configurable hotkeys
- Configurable personality, model, and voice settings

## Notes

This project is designed to run locally.

API keys and other private configuration values should remain in local files that are excluded from version control.
