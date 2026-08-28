# Sample

Counts from #7, measured against the `BTCUSDT` spot archive on `data.binance.vision`. Coverage runs
2017-08-17 to 2026-07-31, 108 months, identical across klines, aggTrades and trades.

| Year | CPI | Employment Situation | FOMC confirmed | FOMC estimated |
| :-- | --: | --: | --: | --: |
| 2017 | 4 | 4 | 0 | 3 |
| 2018 | 12 | 12 | 0 | 8 |
| 2019 | 12 | 12 | 0 | 8 |
| 2020 | 12 | 12 | 0 | 10 |
| 2021 | 12 | 12 | 8 | 0 |
| 2022 | 12 | 12 | 8 | 0 |
| 2023 | 12 | 12 | 8 | 0 |
| 2024 | 12 | 12 | 8 | 0 |
| 2025 | 12 | 12 | 8 | 0 |
| 2026 | 7 | 7 | 5 | 0 |
| **Total** | **107** | **107** | **45** | **29** |

CPI and Employment Situation counts are ceilings from publication cadence, one per covered month;
the July 2017 releases (2017-08-11 and 2017-08-04) precede coverage. FOMC dates for 2021 onward are
from the Federal Reserve calendar; 2017 to 2020 is a cadence estimate including two unscheduled
March 2020 statements, and is unverified. Verified dates are #8's output, and the numbers here are
revised when that lands.

Price coverage is complete at one row per second from 2017-09-01 onward; 2017-08-17, the listing
day, has 71,972 of 86,400 seconds. Binance emits no kline for a second without a trade, so row count
is a liquidity floor rather than a file-integrity check.

## Primary sample

CPI and the Employment Situation, 214 events. Both release at 08:30 ET with no second scheduled
release inside the one-hour window.

FOMC is excluded from the primary sample and retained as a robustness check: the chair's press
conference at 14:30 ET falls inside the window, so $m_e(H)$ would measure the statement and the
press conference jointly. ADR 0002 carries the argument.

At $E = 214$ the population spread $\sigma$ in `fraction-of-move.md` is identified but not
precisely: the year and release-type contrasts are the constrained comparisons, not the pooled
half-time. Dropping events after inspecting them is excluded; exclusion rules are fixed in
`PREREGISTRATION.md`.
