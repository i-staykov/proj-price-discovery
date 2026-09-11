# Concurrent-release source audit

Date: 2026-09-11. Issues: #41, #78. This is a source-feasibility audit, not a completed event screen.
No price rows were read. Missing coverage is unknown, not evidence of an empty release window.

| Source | Evidence available | Unresolved coverage |
| :-- | :-- | :-- |
| BLS | [Annual schedule archive](https://www.bls.gov/bls/archived_sched.htm); sampled annual pages contain dates and ET times | Direct requests returned 403; the schedule describes coverage of “most” national-office releases, so the publication inventory needs an explicit boundary |
| DOL | [Claims archive](https://oui.doleta.gov/unemploy/claims_arch.asp), annual form using POST `report=press&year=YYYY`, and dated PDF embargo headers | Official host `oui.doleta.gov` is excluded by #41's `dol.gov` rule; claims alone do not establish all-agency negatives |
| Census | [Recent calendar](https://www.census.gov/economic-indicators/calendar-listview.html), annual HTML from 2021, and individual release archives | Historical-looking 2017 to 2020 URLs returned newer content with HTTP 200; surviving planned calendars are not final publication inventories |
| BEA | [News archive](https://www.bea.gov/news/archive) with historical-year selector and pagination; dated release headers | Early schedule routes are empty or missing. Reconcile news releases with data-only publications and discontinued products |
| FRB | [Monthly calendar archive](https://www.federalreserve.gov/newsevents/calendar-archive.htm) and [G.17 release dates](https://www.federalreserve.gov/releases/g17/release_dates.htm) | Calendar and actual release archives disagree on some rescheduled dates |
| NYFed | [Empire State](https://www.newyorkfed.org/survey/empire/empiresurvey_archives) and [Business Leaders](https://www.newyorkfed.org/survey/business_leaders/bls_archives) histories | Older general calendars redirect to “Page Not Found”; survey-only inventories omit other publications and revisions |
| PhillyFed | [Manufacturing survey archive](https://www.philadelphiafed.org/surveys-and-data/regional-economic-analysis/manufacturing-business-outlook-survey) with dated PDF headers | Monthly survey archives do not cover all revisions; historical general calendars were not recovered |

## Checks that rule out shortcuts

- DOL released claims on [Wednesday 2021-11-10](https://oui.doleta.gov/press/2021/111021.pdf), a
  primary CPI date. A Thursday-only rule misses a concurrent release.
- Census [retail sales on 2017-10-13](https://www2.census.gov/retail/releases/historical/marts/adv1709.pdf)
  and BEA [travel and tourism on 2017-12-13](https://www.bea.gov/news/2017/travel-and-tourism-satellite-accounts-3rd-quarter-2017)
  have 08:30 headers. A short list of headline indicators is insufficient.
- The FRB [December 2025 calendar](https://www.federalreserve.gov/newsevents/2025-december.htm)
  lists G.17 on December 23; release headers establish both
  [December 3](https://www.federalreserve.gov/releases/g17/20251203/g17.txt) and
  [December 23](https://www.federalreserve.gov/releases/g17/20251223/g17.txt), at 09:15 ET.
- The PhillyFed [current calendar](https://www.philadelphiafed.org/calendar-of-events) includes
  nonmanufacturing historical revisions at 08:30 on primary date 2026-01-13. Survey-release cadence
  alone does not cover that publication.

## Required decision

Issue #78 must fix admissible official hosts, schedule versus publication evidence, the product
inventory and an explicit unknown-coverage state. Then every primary date needs a cited positive
row or verified negative for each source. Neither a successful HTTP response nor an absent search
result establishes a negative. No concurrent flags or empty-release rows are committed by this audit.
