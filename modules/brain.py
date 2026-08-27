"""
Command parser. Turns raw transcribed text into (intent, params).

This starts rule-based (fast, predictable, no extra dependency) so you can
trust exactly what it will do. Swap `parse_command` for a local LLM call
(e.g. via Ollama) later if you want fuzzier natural-language understanding.
"""

import re

INTENT_PATTERNS = [
    ("open_app", r"open (.+)"),
    ("close_app", r"close (.+)"),
    ("search_web", r"search (?:for )?(.+)"),
    ("open_website", r"go to (.+)"),
    ("type_text", r"type (.+)"),
    ("read_screen", r"read (?:the )?screen"),
    ("screenshot", r"take a screenshot"),
    ("volume_up", r"volume up"),
    ("volume_down", r"volume down"),
    ("mute", r"mute"),
    ("click", r"click"),
    ("move_mouse", r"move mouse to (\d+)[, ]+(\d+)"),
    ("shutdown", r"shut ?down"),
    ("restart", r"restart"),
    ("stop", r"^(stop|exit|quit|goodbye)$"),
]


def parse_command(text: str):
    text = text.lower().strip()

    for intent, pattern in INTENT_PATTERNS:
        match = re.search(pattern, text)
        if match:
            return {"intent": intent, "groups": match.groups(), "raw": text}

    return {"intent": "unknown", "groups": (), "raw": text}