"""
Open and close applications across Windows, macOS, and Linux.
"""

import platform
import subprocess
import psutil

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
    closed = False
    for proc in psutil.process_iter(["name"]):
        try:
            if app_name in (proc.info["name"] or "").lower():
                proc.terminate()
                closed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return f"Closed {app_name}" if closed else f"Couldn't find a running app called {app_name}"