"""
Mouse and keyboard automation via pyautogui.
pyautogui works the same across Windows, macOS, and Linux.

Safety note: pyautogui's FAILSAFE is left ON (default). Slam your mouse
to a screen corner at any point to instantly abort an automation in progress.
"""

import pyautogui

pyautogui.PAUSE = 0.2  # small delay between actions so the OS keeps up


def move_mouse(x: int, y: int):
    pyautogui.moveTo(int(x), int(y), duration=0.3)
    return f"Moved mouse to ({x}, {y})"


def click(x: int = None, y: int = None):
    if x is not None and y is not None:
        pyautogui.click(int(x), int(y))
    else:
        pyautogui.click()
    return "Clicked"


def type_text(text: str):
    pyautogui.typewrite(text, interval=0.02)
    return f"Typed: {text}"


def press_key(key: str):
    pyautogui.press(key)
    return f"Pressed {key}"


def hotkey(*keys):
    pyautogui.hotkey(*keys)
    return f"Pressed {'+'.join(keys)}"