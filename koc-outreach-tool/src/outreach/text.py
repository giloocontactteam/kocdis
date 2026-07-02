"""String helpers shared across the toolkit."""
from __future__ import annotations

import re
import urllib.parse
from typing import Optional

# Values that mean "no data" in the source sheet (incl. Chinese placeholders).
PLACEHOLDERS = {"", "nan", "待確認", "待複查", "none", "n/a"}

_HANDLE_FROM_URL_RE = re.compile(r"instagram\.com/([A-Za-z0-9._]+)")
_IG_PATH_WORDS = {"p", "reel", "reels", "explore", "stories", "tv", "accounts", ""}


def clean(value: Optional[str]) -> str:
    """Strip a cell value, returning "" for known placeholders."""
    s = (value or "").strip()
    return "" if s.lower() in PLACEHOLDERS else s


def normalize_handle(handle: str, url: str = "") -> str:
    """Derive a bare IG handle (no @) from a handle cell or an instagram URL."""
    h = clean(handle)
    if h:
        h = h.lstrip("@").strip().strip("/")
        h = re.split(r"[\s(]", h)[0]  # drop stray text like "@foo (bar)"
        if h:
            return h
    u = clean(url)
    if u:
        m = _HANDLE_FROM_URL_RE.search(u)
        if m and m.group(1).lower() not in _IG_PATH_WORDS:
            return m.group(1)
    return ""


def domain_of(url: str) -> str:
    """Return the bare registered domain of a URL (www. stripped)."""
    try:
        net = urllib.parse.urlparse(url if "://" in url else "http://" + url).netloc.lower()
        return net[4:] if net.startswith("www.") else net
    except Exception:
        return ""
