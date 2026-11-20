# news-image-20261120

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/meongs123/news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/meongs123/news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120)

A [make.fun](https://make.fun/bounty/news-image-20261120) entry for
**"Sum up 20 November's world news in one image"** (competition
`news-image-20261120`, $250 prize pool, top 50 paid).

## What this is

One image that sums up the world's news of Friday 20 November 2026.
The program is [`main.ts`](main.ts) (Node 22, standard library only, no
network): it reads `entry.png` from the repository root and copies it
byte-identical to `/output/entry.png`. Running it twice produces
identical bytes.

## Status

Skeleton only, 20 November 2026. The image itself is **not in this
repository yet** — no placeholder or blank image is committed. The final
`entry.png` (PNG or JPEG, ≤ 1 MiB, ≤ 1024×1024) lands on the morning of
21 November 2026, after the final evening news sweep of 20 November,
so the image can cover the full day's news. Nothing else is read by the
judge: it sees exactly the bytes in `entry.png`.

## Run locally

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png`, a byte-identical copy of `entry.png`.

## License

MIT — see [LICENSE](LICENSE).
