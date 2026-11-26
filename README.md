# THE WORLD IN ONE DAY — Thursday 26 November 2026

[![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/Djebrix/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/Djebrix/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

A newspaper-style front page that sums up the world's news of Thursday
26 November 2026 in a single image: the lead story, seven more stories with
drawn scenes, an "Also today" strip and a sources footer.

## What the program does

`main.py` (Python 3, standard library only, no network) draws the front
page with its own 5x7 bitmap font and its own PNG encoder and writes
`/output/entry.png` — a 1024x1024 PNG, well under the 1 MiB limit.
It honours `MAKEFUN_OUTPUT_DIR` when set (default `/output`) and is fully
deterministic: two runs produce byte-identical output.

## How to run

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## The stories (all of 26 November 2026)

1. **Trump hits 14 partners with new tariffs** — Washington unveils
   country-by-country tariffs on 14 economies, including China, the EU,
   Japan and India. Sources: One Turn day digest, Open Chronicle global
   news brief, Morning Briefing #228.
2. **Houthis strike Saudi ports and refinery** — Houthis claim hits on
   Jeddah and Jizan ports and the Ras Tanura refinery. Sources: One Turn,
   Newsquawk European opening news.
3. **EU split over 45bn Ukraine loan** — Leaders meet in Brussels over a
   EUR 45 billion loan for Ukraine and the 2028–2034 budget. Source:
   Daily Summary Of, 26 November 2026.
4. **Kim orders more tactical nukes** — Kim Jong Un says North Korea
   should deploy tactical nuclear weapons across more domains (KCNA).
   Sources: Daily Summary Of, Open Chronicle.
5. **Ukraine hits airbase; Kyiv under fire** — Kyiv says five jets were
   damaged at Savasleyka airbase; Russia answers with ballistic missiles
   on Kyiv. Sources: Daily Summary Of, One Turn, Morning Briefing #228.
6. **Israeli strikes kill nine in Gaza** — Overnight strikes kill at least
   nine Palestinians, medics say. Source: Morning Briefing #228.
7. **Cairo tanker fire kills at least 31** — A fuel tanker overturns on
   the Ring Road in Warraq, Giza; 31 dead, 21 hurt; driver detained.
   Sources: AP (via Irish Times), Daily Fox News.
8. **13 miners trapped in flooded mine** — Rescuers race to reach 13
   miners trapped in a flooded gold mine in Bogor, Indonesia. Source:
   Daily Summary Of.

Also today: the 100th Macy's Thanksgiving Day Parade in New York; Puerto
Rico's Supreme Court cancels the Luma Energy power contract; the Nasdaq
nears a bear market; Liverpool beat Club Brugge 3–0.

## License

MIT — see `LICENSE`.
