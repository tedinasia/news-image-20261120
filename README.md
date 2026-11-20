# The World Today — 20 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/tedinasia/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/tedinasia/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

A [make.fun](https://make.fun/bounty/news-image-20261120) bounty entry: a program that draws a newspaper front page summing up the world's news of Friday 20 November 2026 — the Trump–Xi–Putin summit in Shenzhen and its peace declaration, Anthropic's record $81.3bn IPO, the UN court's ruling that Myanmar committed genocide against the Rohingya, the tanker fire in the Strait of Hormuz, a fifth straight daily fall for the S&P 500, and Cyclone Akvan's landfall in Odisha — as one 1024×1024 image.

## Run it

```sh
python3 main.py            # writes /output/entry.png
python3 main.py entry.png  # or write to a path of your choice
```

The program uses only Pillow and the standard library, needs no network, and is deterministic: two runs write byte-identical PNG files.

## The image

`main.py` draws the whole front page with Pillow — masthead, lead story with a Shenzhen skyline, three story cards, the markets and cyclone rows, and a footer ticker. `entry.png` is the program's output, kept in the repo as a preview.

Bounty: https://make.fun/bounty/news-image-20261120
