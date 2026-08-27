"""
AI Voice Assistant - core loop.

Flow: press Enter to talk -> record -> transcribe (local Whisper) ->
parse intent -> execute action -> speak result.

Push-to-talk (press Enter) is used instead of an always-on wake word to
start with. It's simpler, uses zero extra API keys, and avoids the assistant
mishearing background noise as a command. A wake-word engine (e.g. Porcupine)
can be dropped in later once the command set is solid.
"""

from modules import stt, tts, brain
from modules.actions import (  # pyright: ignore[reportMissingImports]
    app_control,
    browser_control,
    system_control,
    input_control,
    screen_reader,
)

# Commands that must never fire without a spoken "yes"
DESTRUCTIVE_INTENTS = {"shutdown", "restart"}


def execute(command: dict) -> str:
    intent = command["intent"]
    groups = command["groups"]

    if intent == "open_app":
        return app_control.open_app(groups[0])
    if intent == "close_app":
        return app_control.close_app(groups[0])
    if intent == "search_web":
        return browser_control.search_web(groups[0])
    if intent == "open_website":
        return browser_control.open_website(groups[0])
    if intent == "type_text":
        return input_control.type_text(groups[0])
    if intent == "click":
        return input_control.click()
    if intent == "move_mouse":
        return input_control.move_mouse(groups[0], groups[1])
    if intent == "read_screen":
        return screen_reader.read_screen()
    if intent == "screenshot":
        path = screen_reader.take_screenshot()
        return f"Screenshot saved to {path}"
    if intent == "volume_up":
        return system_control.volume_up()
    if intent == "volume_down":
        return system_control.volume_down()
    if intent == "mute":
        return system_control.mute()
    if intent == "shutdown":
        return system_control.shutdown(confirmed=True)
    if intent == "restart":
        return system_control.restart(confirmed=True)
    if intent == "stop":
        return "STOP"

    return "Sorry, I didn't understand that command."


def confirm_destructive(intent: str) -> bool:
    tts.speak(f"Are you sure you want to {intent}? Say yes to confirm.")
    reply = stt.listen_and_transcribe(duration=3).lower()
    return "yes" in reply


def main():
    tts.speak("Assistant ready. Press Enter and speak your command.")
    while True:
        input("\n[Press Enter to talk]")
        text = stt.listen_and_transcribe(duration=5)
        if not text:
            tts.speak("I didn't catch that.")
            continue

        print(f"[You said]: {text}")
        command = brain.parse_command(text)

        if command["intent"] in DESTRUCTIVE_INTENTS:
            if not confirm_destructive(command["intent"]):
                tts.speak("Okay, cancelled.")
                continue

        result = execute(command)

        if result == "STOP":
            tts.speak("Goodbye!")
            break

        tts.speak(result)


if __name__ == "__main__":
    main()