# news-front-page-typed

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/ilyayaaa/news-front-page-typed/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/ilyayaaa/news-front-page-typed/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

An illustrated newspaper front page for Saturday 21 November 2026: 31 stories in 7 regions, 15 of them with hand-drawn pictures, a numbered map, an ALSO list and a date check. Every claim comes from the BBC, Al Jazeera and Straits Times RSS feeds of that day.

- `data/stories.json`: the stories and figures, each with the feed item and phrase that backs it.
- `data/feeds/` (git-ignored, kept locally): snapshots of the three RSS feeds, saved from https://feeds.bbci.co.uk/news/world/rss.xml, https://www.aljazeera.com/xml/rss/all.xml and https://www.straitstimes.com/news/world/rss.xml as `bbc.xml`, `aljazeera.xml` and `straitstimes.xml`.
- `tools/verify_facts.py`: checks every claim against those snapshots (set `FEEDS_DIR` to read them from another folder) (item exists, is stamped inside 21 November in some time zone, contains the phrase).
- `tools/scenes.py` and `tools/build_poster.py` (Pillow): draw the illustrations and lay out `assets/entry.png` (1024x1024 PNG); the build stops on any text overflow or overlapping block.
- `main.py` (standard library only): copies `assets/entry.png` to `/output/entry.png`.

## Run it

```sh
python3 tools/verify_facts.py && python3 tools/build_poster.py   # rebuild the image
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py            # what the grader runs
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=rv7zbbj2&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
