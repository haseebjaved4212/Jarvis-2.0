"""
System-level control: volume and power actions.
Shutdown/restart are gated behind explicit confirmation on purpose,
a misheard command should never be able to turn the machine off.
"""

import platform
import subprocess

SYSTEM = platform.system()


def _run(cmd):
    subprocess.run(cmd, shell=True)


def volume_up():
    if SYSTEM == "Windows":
        _run("nircmd.exe changesysvolume 5000" if False else
             'powershell -c "(New-Object -com wscript.shell).SendKeys([char]175)"')
    elif SYSTEM == "Darwin":
        _run('osascript -e "set volume output volume (output volume of (get volume settings) + 10)"')
    else:
        _run("amixer -D pulse sset Master 10%+")
    return "Volume up"


def volume_down():
    if SYSTEM == "Windows":
        _run('powershell -c "(New-Object -com wscript.shell).SendKeys([char]174)"')
    elif SYSTEM == "Darwin":
        _run('osascript -e "set volume output volume (output volume of (get volume settings) - 10)"')
    else:
        _run("amixer -D pulse sset Master 10%-")
    return "Volume down"


def mute():
    if SYSTEM == "Windows":
        _run('powershell -c "(New-Object -com wscript.shell).SendKeys([char]173)"')
    elif SYSTEM == "Darwin":
        _run('osascript -e "set volume output volume 0"')
    else:
        _run("amixer -D pulse sset Master mute")
    return "Muted"


def shutdown(confirmed: bool):
    """Requires explicit confirmation before executing, this is destructive."""
    if not confirmed:
        return "CONFIRM_REQUIRED:shutdown"
    if SYSTEM == "Windows":
        _run("shutdown /s /t 5")
    elif SYSTEM == "Darwin":
        _run("osascript -e 'tell app \"System Events\" to shut down'")
    else:
        _run("shutdown -h now")
    return "Shutting down"


def restart(confirmed: bool):
    if not confirmed:
        return "CONFIRM_REQUIRED:restart"
    if SYSTEM == "Windows":
        _run("shutdown /r /t 5")
    elif SYSTEM == "Darwin":
        _run("osascript -e 'tell app \"System Events\" to restart'")
    else:
        _run("shutdown -r now")
    return "Restarting"