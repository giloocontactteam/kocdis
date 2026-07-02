"""Fetch Instagram profile data through a logged-in browser over CDP.

We attach to an already-authenticated Chrome (see :mod:`outreach.browser`) and
call Instagram's own ``web_profile_info`` web endpoint from the page context, so
requests carry real session cookies and look like normal in-app navigation.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

from .emails import pick_email

CDP_URL = os.environ.get("CHROME_CDP_URL", "http://localhost:9222")
IG_APP_ID = "936619743392459"  # Instagram web client app id


@dataclass
class Profile:
    row_no: str = ""
    name: str = ""
    resolved_handle: str = ""
    profile_url: str = ""
    full_name: str = ""
    is_private: str = ""
    is_business: str = ""
    category: str = ""
    followers: str = ""
    following: str = ""
    posts: str = ""
    email: str = ""
    website: str = ""
    bio: str = ""
    status: str = ""


def connect(playwright, cdp_url: str = CDP_URL):
    """Connect to the debug Chrome and return (browser, context, page)."""
    browser = playwright.chromium.connect_over_cdp(cdp_url)
    ctx = browser.contexts[0] if browser.contexts else browser.new_context()
    return browser, ctx, ctx.new_page()


def _csrf_from_cookies(page) -> str:
    try:
        for c in page.context.cookies("https://www.instagram.com"):
            if c.get("name") == "csrftoken":
                return c.get("value", "")
    except Exception:
        pass
    return ""


def fetch_profile_json(page, handle: str, csrf: str) -> dict:
    """Call web_profile_info from the page; return {"_status": int, "body": ...}."""
    return page.evaluate(
        """async ([handle, appId, csrf]) => {
            const url = `/api/v1/users/web_profile_info/?username=${encodeURIComponent(handle)}`;
            try {
                const r = await fetch(url, {headers: {
                    'x-ig-app-id': appId, 'x-csrftoken': csrf,
                    'x-requested-with': 'XMLHttpRequest'}});
                let body = null; try { body = await r.json(); } catch (e) {}
                return { _status: r.status, body };
            } catch (e) { return { _status: -1, _err: String(e) }; }
        }""",
        [handle, IG_APP_ID, csrf],
    )


def scrape_profile(page, handle: str, fallback_email: str = "") -> Profile:
    """Fetch one profile; status is one of ok/timeout/login_required/not_found/..."""
    res = Profile(resolved_handle=handle)
    res.profile_url = f"https://www.instagram.com/{handle}/"
    try:
        page.goto(res.profile_url, wait_until="domcontentloaded", timeout=30000)
    except PWTimeout:
        res.status, res.email = "timeout", fallback_email
        return res

    if "/accounts/login" in page.url:
        res.status, res.email = "login_required", fallback_email
        return res

    try:
        payload = fetch_profile_json(page, handle, _csrf_from_cookies(page))
    except Exception as e:  # noqa: BLE001
        res.status, res.email = f"error: {type(e).__name__}", fallback_email
        return res

    status = payload.get("_status")
    if status == 404:
        res.status, res.email = "not_found", fallback_email
        return res
    if status in (401, 403):
        res.status, res.email = "login_required", fallback_email
        return res

    user = ((payload.get("body") or {}).get("data") or {}).get("user")
    if not user:
        res.status, res.email = f"no_data (http {status})", fallback_email
        return res

    bio = (user.get("biography") or "").strip()
    res.full_name = (user.get("full_name") or "").strip()
    res.bio = " ".join(bio.split())[:500]
    res.website = user.get("external_url") or ""
    res.is_private = "yes" if user.get("is_private") else "no"
    res.is_business = "yes" if user.get("is_business_account") else "no"
    res.category = user.get("category_name") or user.get("category") or ""
    res.followers = str((user.get("edge_followed_by") or {}).get("count", "") or "")
    res.following = str((user.get("edge_follow") or {}).get("count", "") or "")
    res.posts = str((user.get("edge_owner_to_timeline_media") or {}).get("count", "") or "")
    res.email = pick_email(
        user.get("business_email") or "",
        user.get("public_email") or "",
        bio,
        fallback_email,
    )
    res.status = "ok"
    return res


__all__ = ["Profile", "CDP_URL", "IG_APP_ID", "connect", "scrape_profile",
           "fetch_profile_json", "sync_playwright"]
