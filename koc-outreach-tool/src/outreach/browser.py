"""Start an authenticated headless debug Chrome without quitting your main Chrome.

Your real Chrome user-data-dir is locked while Chrome runs, so we can't attach a
debug port to it directly. Instead we seed a throwaway profile with just the
login cookies copied from one of your real profiles, then launch a headless
Chrome with remote debugging against that copy.

Cross-platform: the Chrome binary and user-data-dir are auto-detected for macOS,
Linux and Windows. Override either with the CHROME_BINARY / CHROME_USER_DATA
environment variables if your install is non-standard.

Profiles known to hold an Instagram session can be discovered with
``list_ig_profiles()``.
"""
from __future__ import annotations

import os
import platform
import shutil
import sqlite3
import subprocess
import time
import urllib.request

DEBUG_DIR = os.path.expanduser("~/.ig_crawl_debug_profile")
DEFAULT_PORT = 9222

# Candidate Chrome binaries per OS, first existing/​resolvable one wins.
_CHROME_CANDIDATES = {
    "Darwin": [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ],
    "Linux": [
        "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
        "/usr/bin/google-chrome", "/usr/bin/chromium",
    ],
    "Windows": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    ],
}

# Default user-data-dir per OS.
_USER_DATA_CANDIDATES = {
    "Darwin": ["~/Library/Application Support/Google/Chrome"],
    "Linux": ["~/.config/google-chrome", "~/.config/chromium"],
    "Windows": [r"%LOCALAPPDATA%\Google\Chrome\User Data"],
}


def chrome_binary() -> str:
    """Resolve the Chrome/Chromium executable (env override: CHROME_BINARY)."""
    env = os.environ.get("CHROME_BINARY")
    if env:
        return env
    for cand in _CHROME_CANDIDATES.get(platform.system(), []):
        if os.path.isabs(cand) or os.sep in cand:
            if os.path.exists(os.path.expandvars(cand)):
                return os.path.expandvars(cand)
        else:
            found = shutil.which(cand)
            if found:
                return found
    raise FileNotFoundError(
        "Chrome not found. Install Google Chrome or set CHROME_BINARY to its path.")


def chrome_user_data() -> str:
    """Resolve Chrome's user-data-dir (env override: CHROME_USER_DATA)."""
    env = os.environ.get("CHROME_USER_DATA")
    if env:
        return os.path.expanduser(env)
    for cand in _USER_DATA_CANDIDATES.get(platform.system(), []):
        path = os.path.expanduser(os.path.expandvars(cand))
        if os.path.isdir(path):
            return path
    raise FileNotFoundError(
        "Chrome user-data-dir not found. Set CHROME_USER_DATA to your profile dir.")


def cookies_path(user_data: str, profile: str) -> str | None:
    """Locate a profile's Cookies DB across Chrome versions, or None."""
    for rel in (os.path.join(profile, "Network", "Cookies"),
                os.path.join(profile, "Cookies")):
        path = os.path.join(user_data, rel)
        if os.path.isfile(path):
            return path
    return None


def list_ig_profiles() -> list[tuple[str, str]]:
    """Return [(profile_dir, status)] where status is logged_in / cookies / none."""
    user_data = chrome_user_data()
    out = []
    for p in sorted(os.listdir(user_data)):
        db = cookies_path(user_data, p)
        if not db:
            continue
        try:
            con = sqlite3.connect(f"file:{db}?immutable=1", uri=True)
            names = {r[0] for r in con.execute(
                "SELECT name FROM cookies WHERE host_key LIKE '%instagram.com%'")}
            con.close()
        except Exception:
            continue
        if "sessionid" in names:
            status = "logged_in"
        elif names:
            status = "cookies"
        else:
            status = "none"
        out.append((p, status))
    return out


def port_up(port: int = DEFAULT_PORT) -> bool:
    try:
        urllib.request.urlopen(f"http://localhost:{port}/json/version", timeout=1)
        return True
    except Exception:
        return False


def seed_and_launch(profile: str = "Default", port: int = DEFAULT_PORT,
                    debug_dir: str = DEBUG_DIR) -> subprocess.Popen:
    """Copy ``profile``'s cookies into a debug dir and launch headless Chrome."""
    chrome = chrome_binary()
    user_data = chrome_user_data()
    cookies = cookies_path(user_data, profile)
    if not cookies:
        raise FileNotFoundError(
            f"No Cookies DB for profile {profile!r} under {user_data}. "
            f"Run with --list to see available profiles.")
    os.makedirs(os.path.join(debug_dir, "Default"), exist_ok=True)
    local_state = os.path.join(user_data, "Local State")
    if os.path.exists(local_state):
        shutil.copy2(local_state, os.path.join(debug_dir, "Local State"))
    shutil.copy2(cookies, os.path.join(debug_dir, "Default", "Cookies"))

    proc = subprocess.Popen(
        [chrome, f"--remote-debugging-port={port}", f"--user-data-dir={debug_dir}",
         "--profile-directory=Default", "--headless=new", "--no-first-run",
         "--no-default-browser-check", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(20):
        if port_up(port):
            return proc
        time.sleep(0.5)
    raise RuntimeError(f"debug Chrome did not expose port {port}")


def stop(debug_dir: str = DEBUG_DIR) -> None:
    """Stop the debug Chrome (matched by its unique user-data-dir)."""
    if platform.system() == "Windows":
        subprocess.run(["taskkill", "/F", "/IM", "chrome.exe"], check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        subprocess.run(["pkill", "-f", f"user-data-dir={debug_dir}"], check=False)
