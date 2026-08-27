"""
Open and close applications across Windows, macOS, and Linux.
"""

import platform
import subprocess

SYSTEM = platform.system()  # "Windows", "Darwin", or "Linux"


def open_app(app_name: str):
    app_name = app_name.strip()
    try:
        if SYSTEM == "Windows":
            subprocess.Popen(f"start {app_name}", shell=True)
        elif SYSTEM == "Darwin":
            subprocess.Popen(["open", "-a", app_name])
        else:  # Linux
            subprocess.Popen([app_name.lower()])
        return f"Opening {app_name}"
    except Exception as e:
        return f"Couldn't open {app_name}: {e}"


def close_app(app_name: str):
    app_name = app_name.strip().lower()
    try:
        if SYSTEM == "Windows":
            result = subprocess.run(
                ["taskkill", "/IM", app_name, "/T", "/F"],
                capture_output=True,
                text=True,
            )
        elif SYSTEM == "Darwin":
            result = subprocess.run(["pkill", "-f", app_name], capture_output=True)
        else:  # Linux
            result = subprocess.run(["pkill", "-f", app_name], capture_output=True)

        return (
            f"Closed {app_name}"
            if result.returncode == 0
            else f"Couldn't find a running app called {app_name}"
        )
    except (OSError, subprocess.SubprocessError) as e:
        return f"Couldn't close {app_name}: {e}"