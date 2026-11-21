"""Check every claim in data/stories.json against the saved RSS feeds.

For each check [feed, title-substring, must-substring] the feed item whose title
contains the first substring must exist, must carry a timestamp that falls on
21 November 2026 in some time zone (UTC+14 starts it at 20 Nov 10:00 UTC), and
its title plus description must contain the second substring. Left-out items
must be older than that window. Exit code 1 on any failure.
"""
import datetime
import email.utils
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WINDOW_START = datetime.datetime(2026, 11, 20, 10, 0, tzinfo=datetime.timezone.utc)
WINDOW_END = datetime.datetime(2026, 11, 21, 12, 0, tzinfo=datetime.timezone.utc)


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", html.unescape(s or ""))).strip()


def load_feeds():
    feeds = {}
    feed_dir = os.environ.get("FEEDS_DIR") or os.path.join(ROOT, "data", "feeds")
    for name in ("bbc", "aljazeera", "straitstimes"):
        root = ET.parse(os.path.join(feed_dir, name + ".xml")).getroot()
        items = []
        for it in root.iter("item"):
            when = email.utils.parsedate_to_datetime(it.findtext("pubDate")).astimezone(datetime.timezone.utc)
            items.append((clean(it.findtext("title")), clean(it.findtext("description")), when))
        feeds[name] = items
    return feeds


def walk_checks(data):
    for n in data["numbers"]:
        yield "number " + n["value"], n["checks"]
    for s in data["big"] + data["mini"]:
        yield f"story {s['n']} {s['headline']}", s["checks"]
    for s in data["also"]:
        yield f"also {s['n']}", s["checks"]


def main():
    with open(os.path.join(ROOT, "data", "stories.json"), encoding="utf-8") as f:
        data = json.load(f)
    feeds = load_feeds()
    bad = 0
    total = 0
    for label, checks in walk_checks(data):
        for feed, title_part, must in checks:
            total += 1
            hits = [i for i in feeds[feed] if title_part.lower() in i[0].lower()]
            if not hits:
                print(f"FAIL {label}: no {feed} item titled like {title_part!r}")
                bad += 1
                continue
            title, desc, when = hits[0]
            if not WINDOW_START <= when <= WINDOW_END:
                print(f"FAIL {label}: {title!r} is dated {when:%d %b %H:%M} UTC, outside the 21 Nov window")
                bad += 1
            if must.lower() not in (title + " " + desc).lower():
                print(f"FAIL {label}: {must!r} not found in {title!r}")
                bad += 1
    for feed, title_part in data["left_out"]:
        hits = [i for i in feeds[feed] if title_part.lower() in i[0].lower()]
        if not hits or hits[0][2] >= WINDOW_START:
            print(f"FAIL left-out item {title_part!r} is missing or inside the window")
            bad += 1
    nums = len(data["big"]) + len(data["mini"]) + len(data["also"])
    if nums != 31 or [s["n"] for s in data["big"] + data["mini"] + data["also"]] != list(range(1, 32)):
        print("FAIL story numbering is not 1..31")
        bad += 1
    print(f"{total} checks, {bad} failures")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
