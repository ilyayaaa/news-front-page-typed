# World news front page, Saturday 21 November 2026

An entry for make.fun's `news-image-20261121` bounty: one image that sums up the
day's world news as an illustrated newspaper front page (31 stories, 7 regions).

- `data/stories.json`: the stories, figures and, for each claim, the feed item and
  phrase that backs it.
- `data/feeds/`: snapshots of the BBC, Al Jazeera and Straits Times RSS feeds the
  facts come from.
- `tools/verify_facts.py`: checks every claim against those snapshots (the item must
  exist, be stamped inside 21 November in some time zone, and contain the phrase).
- `tools/scenes.py` (Pillow): the hand-drawn illustrations.
- `tools/build_poster.py` (Pillow): lays out and draws `assets/entry.png`
  (1024x1024 PNG) and stops on any text overflow or overlapping block.
- `main.py` (standard library only): copies `assets/entry.png` to `/output/entry.png`.

Rebuild: `python3 tools/verify_facts.py && python3 tools/build_poster.py`.
