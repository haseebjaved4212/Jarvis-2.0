"""
Text-to-speech module. Offline, uses the OS-native voice engine via pyttsx3.
Works on Windows (SAPI5), macOS (NSSpeechSynthesizer), and Linux (espeak).
"""

import importlib

_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        try:
            pyttsx3 = importlib.import_module("pyttsx3")
        except ImportError as exc:
            raise RuntimeError(
                "pyttsx3 is not installed. Run: python -m pip install pyttsx3"
            ) from exc
        _engine = pyttsx3.init()
        _engine.setProperty("rate", 175)
    return _engine


def speak(text: str):
    print(f"[Assistant]: {text}")
    engine = _get_engine()
    engine.say(text)
    engine.runAndWait()