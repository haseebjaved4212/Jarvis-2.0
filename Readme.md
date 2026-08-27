# AI Voice Assistant

Offline, cross-platform voice assistant that controls your PC: launches apps,
searches the web, automates mouse/keyboard, reads text off your screen, and
handles system commands like volume and shutdown.

## How it works

Push-to-talk loop: press Enter, speak, and it transcribes locally with
Whisper (no internet, no API key), matches your words to a command, and
runs it. Destructive actions (shutdown, restart) always ask for a spoken
"yes" before executing.

## Setup

1. Install Python 3.10+.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Install Tesseract OCR (needed for "read the screen"):
   - Windows: `choco install tesseract` (or download the installer from the Tesseract GitHub)
   - macOS: `brew install tesseract`
   - Linux: `sudo apt install tesseract-ocr`
4. Run it:
   ```
   python main.py
   ```

## Commands it understands right now

- "open [app name]" / "close [app name]"
- "search for [query]"
- "go to [website]"
- "type [text]"
- "click"
- "move mouse to [x] [y]"
- "read the screen"
- "take a screenshot"
- "volume up" / "volume down" / "mute"
- "shutdown" / "restart" (asks for confirmation first)
- "stop" / "exit" / "quit"

## Project structure

```
Jarvis-2.0/
  main.py                       # core loop
  modules/
    stt.py                      # offline speech-to-text (faster-whisper)
    tts.py                      # offline text-to-speech (pyttsx3)
    brain.py                    # command parser (text -> intent)
    actions/
      app_control.py            # open/close apps
      browser_control.py        # web search, open sites
      system_control.py         # volume, shutdown, restart
      input_control.py          # mouse/keyboard automation
      screen_reader.py          # screenshot + OCR
```

## Where to go next

This is a working skeleton, not the finished "controls everything" version.
Realistic next steps, roughly in order of value:

1. **Test each command on your actual machine** before adding more. App names
   differ per OS (e.g. `open_app` on Linux assumes the binary name matches
   what you say).
2. **Swap `brain.py`'s regex parser for a local LLM** (via Ollama) once the
   rule-based version feels limiting, this is what lets you say things in a
   more natural, less rigid way.
3. **Add a real wake word** (Porcupine, or an open-source alternative) once
   you're happy with push-to-talk and want hands-free activation.
4. **Expand `input_control.py`** for more complex automations: drag, scroll,
   window snapping.
5. **Harden confirmations**: right now only shutdown/restart require a "yes".
   Consider adding it to close_app or anything that could lose unsaved work.