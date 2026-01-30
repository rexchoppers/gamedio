# Gamedio

Lightweight script that reads your currently playing Spotify track, generates a short radio-style shout-out using a local LLM, copies the announcement to the clipboard, and simulates typing/pasting it into the current window

# Background

When playing [Holdfast: Nations At War](https://steamcommunity.com/app/589290), I often indulge in playing the weirdest songs down a virtual audio cable. However, I often get questions such as: 

- `What is that song?`
- `Who is playing that terrible music?` 
- `omg stfu`

Therefore, I decided to make a this small script to essentially create a radio presenter for the currently playing Spotify song.


# Getting Started

Quick start

1. Install Python 3.12 (recommended) and create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate