"""Unit tests for the pure helpers (no browser/network needed).

Run:  python3 -m pytest tests/ -q      (or: python3 tests/test_helpers.py)
"""
from outreach.text import clean, normalize_handle, domain_of
from outreach.emails import good_emails, best_email, pick_email


def test_clean_placeholders():
    assert clean("待確認") == ""
    assert clean("  nan ") == ""
    assert clean(" @foo ") == "@foo"


def test_normalize_handle():
    assert normalize_handle("@NQAPIA", "") == "NQAPIA"
    assert normalize_handle("待確認", "https://www.instagram.com/framelinefest/") == "framelinefest"
    assert normalize_handle("@foo (bar)", "") == "foo"
    assert normalize_handle("待確認", "https://www.instagram.com/p/abc/") == ""  # skip post URLs


def test_domain_of():
    assert domain_of("https://www.frameline.org/contact") == "frameline.org"
    assert domain_of("qwocmap.org") == "qwocmap.org"


def test_good_emails_filters_junk():
    text = "reach info@frameline.org or logo@2x.png or no-reply@x.com"
    emails = good_emails(text)
    assert "info@frameline.org" in emails
    assert all("@2x" not in e and "no-reply" not in e for e in emails)


def test_best_email_prefers_domain_then_contact_prefix():
    cands = ["random@gmail.com", "info@frameline.org"]
    assert best_email(cands, prefer_domain="frameline.org") == "info@frameline.org"
    assert best_email(["x@a.com", "hello@b.com"]) == "hello@b.com"


def test_pick_email_scans_in_order():
    assert pick_email("", "no email here", "ping me at a@b.org") == "a@b.org"
    assert pick_email("first@a.com second@b.com") == "first@a.com"


if __name__ == "__main__":
    import sys
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\n{len(fns)} tests passed")
    sys.exit(0)
