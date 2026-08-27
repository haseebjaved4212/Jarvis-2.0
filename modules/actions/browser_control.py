"""
Browser control. Uses the default system browser, works the same on every OS.
"""

import webbrowser


def search_web(query: str):
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Searching for {query}"


def open_website(site: str):
    site = site.strip()
    if not site.startswith("http"):
        site = f"https://{site}"
    webbrowser.open(site)
    return f"Opening {site}"