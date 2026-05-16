# Leipov Twitch Bot

Leipov is a local Twitch chat assistant built in Python. It connects to Twitch chat, listens for messages or commands, and responds using a custom AI personality.

Leipov does not like the streamer very much, but he finds most humans pretty alright.

## Important First Step

This project will not run correctly until you create a local API key file.

In the same folder as `leipov.py`, create a file named:

    leipovkey.txt

Inside that file, paste your OpenAI API key by itself:

    sk-your-api-key-goes-here

Do not include extra text, quotes, spaces, or labels.

This file is read by the bot when it starts. The API key file is kept separate from the code so the key does not get uploaded to GitHub.

## API Key Warning

Never upload your API key to GitHub.

Make sure `.gitignore` includes:

    leipovkey.txt
    venv/
    __pycache__/
    *.pyc
    .env

If you accidentally commit your API key, delete it from the repo and rotate the API key immediately.

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

If everything is set up correctly, Leipov should connect to Twitch chat and start listening for messages.

## Parts You May Need To Change

Some parts of the code are marked with long comment dividers like this:

    ##############################

These are sections that may need to be customized depending on your stream setup, Twitch channel, bot behavior, prompts, or file paths.

More important sections are marked with larger boxed comments, like this:

    ##############################
    #                            #
    # IMPORTANT SETTINGS HERE    #
    #                            #
    ##############################

Those boxed sections are the main places to check first if the bot does not connect, responds weirdly, or needs to be adjusted for a different streamer.

Common things you may need to change include:

- Bot name
- Bot OAuth token or login method
- Personality prompt
- Screenshot hotkey
- Screenshot monitor settings
- Response cooldowns
- Model name
- File paths
- Debug mode settings

## Features

- Connects to Twitch chat
- Reads chat messages in real time
- Sends AI generated responses
- Uses a custom personality prompt
- Supports local API key storage
- Includes optional screenshot support
- Can be expanded with hotkeys, commands, cooldowns, and moderation tools

## Tech Stack

- Python
- Twitch chat connection
- OpenAI API
- MSS for screenshots
- Local configuration files

## Project Goals

The goal of this project is to create a lightweight AI powered stream companion that feels more like a character than a standard chatbot.

Instead of only responding to fixed commands, Leipov can react to chat messages with personality and context.

This project also acts as a practical example of:

- Real time chat automation
- API integration
- Prompt engineering
- Local config management
- Streamer focused tooling
- Python event handling

## Current Status

This project is currently a working prototype. Core chat response behavior is functional, and additional stream utility features are being tested.

## Planned Features

- Control panel UI
- Better command handling
- Message cooldowns
- Screenshot hotkey support
- Multi monitor screenshot mode
- Persona editor
- Stream safe response filters
- Config file for channel name and bot settings
- Better logging
- Optional text to speech support

## Example Use Cases

- AI stream companion
- Twitch chat personality bot
- Stream joke responder
- Screenshot aware assistant
- Local streamer utility bot
- Experimental AI character system

## Notes

This project is meant to run locally. API keys and private stream settings should be stored in ignored local files and should never be committed to the repository.