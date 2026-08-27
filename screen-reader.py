"""
Reads on-screen text using a screenshot + OCR (pytesseract).
Requires the Tesseract OCR binary to be installed on the system separately
(brew install tesseract / apt install tesseract-ocr / choco install tesseract).
"""

import pyautogui
import pytesseract


def take_screenshot(path="screenshot.png"):
    img = pyautogui.screenshot()
    img.save(path)
    return path


def read_screen():
    img = pyautogui.screenshot()
    text = pytesseract.image_to_string(img)
    text = text.strip()
    return text if text else "I couldn't find any readable text on screen."