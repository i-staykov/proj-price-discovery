# Sample

Counts from the verified release calendar (#17), `src/pricediscovery/release_calendar.csv`, over
2017-09-01 to 2026-07-31. Price coverage from `data.binance.vision` runs 2017-08-17 to 2026-07-31,
108 months, identical across klines, aggTrades and trades.

| Year | CPI | Employment Situation | FOMC |
| :-- | --: | --: | --: |
| 2017 | 4 | 4 | 3 |
| 2018 | 12 | 12 | 8 |
| 2019 | 12 | 12 | 8 |
| 2020 | 12 | 12 | 7 |
| 2021 | 12 | 12 | 8 |
| 2022 | 12 | 12 | 8 |
| 2023 | 12 | 12 | 8 |
| 2024 | 12 | 12 | 8 |
| 2025 | 11 | 11 | 8 |
| 2026 | 7 | 7 | 5 |
| **Total** | **106** | **106** | **71** |

CPI and Employment Situation dates are the ALFRED vintage dates of the non-seasonally-adjusted
headline series `CPIAUCNS` and `PAYNSA`; FOMC statement dates are the regularly scheduled meetings
on the Federal Reserve calendars. Method and rejected alternatives are in ADR 0003. The July 2017
releases (2017-08-11, 2017-08-04) precede price coverage. 2025 is 11, not 12, for both series: no
CPI was released in November 2025 and the October 2025 Employment Situation was cancelled, both from
the federal shutdown (ADR 0001). FOMC 2020 is 7, not 8: the 17-18 March meeting was cancelled and
its replacement, the 15 March intermeeting cut, is out of scope (ADR 0001).

Six sampled days between 2017-09-01 and 2022-06-10 each have 86,400 rows; the 2017-08-17 listing day
has 71,972. This checks the sample dates, not every day in the archive.

## Primary sample

CPI and the Employment Situation, 212 events. Both release at 08:30 ET with no second scheduled
release inside the one-hour window.

FOMC is excluded from the primary sample and retained as a robustness check: the chair's press
conference at 14:30 ET falls inside the window, so $m_e(H)$ would measure the statement and the
press conference jointly. ADR 0002 carries the argument.

The 212 events motivate partial pooling. Precision is assessed by simulation and posterior
diagnostics. Exclusion rules are fixed in `PREREGISTRATION.md`.
