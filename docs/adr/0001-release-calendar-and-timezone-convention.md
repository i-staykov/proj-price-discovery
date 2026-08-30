# 0001 Release calendar sources and the timezone convention

Status: accepted
Date: 2026-08-25
Issue: #8

## Context

CPI, the Employment Situation, and FOMC statements are scheduled in US Eastern local time, but the
price data is indexed in UTC. Eastern local time is not a fixed UTC offset: it is UTC-5 (EST) from
early November to mid-March and UTC-4 (EDT) the rest of the year, per US daylight saving rules. A
release timestamp stored as a naive local time, or converted with a hardcoded offset, is wrong for
half the year and wrong in a way that does not crash — it silently misaligns the event window by an
hour. `cpi-kill-check.ipynb` already avoids this by storing `EVENT_LOCAL_TIME = (8, 30, 0)` and
converting through a `tz`-aware `pandas.Timestamp` (`.tz_localize("America/New_York").tz_convert("UTC")`).
This ADR generalizes that pattern to all three release types and records where the source dates come
from.

## Decision

Release times are stored as local wall-clock time in the `America/New_York` IANA zone and converted
to UTC at load time via the IANA tz database (`zoneinfo`/`pandas`), never with a fixed offset. The
conversion happens once, in the calendar-loading step, so every downstream consumer works in UTC only.

Scheduled times, confirmed against each source below:

- CPI and the Employment Situation: 08:30 ET.
- FOMC statements, regularly scheduled meetings only: 14:00 ET, in effect since March 2013.

Sources for the calendar dates:

- FOMC meeting dates: <https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm>. Rolling
  window, currently 2021-2027 (checked 2026-08-25). Earlier years live at
  `fomchistorical{YYYY}.htm` on the same host. It is an HTML table, not a feed; a scraper has to
  parse the table rather than call a structured endpoint.
- BLS CPI schedule: <https://www.bls.gov/schedule/news_release/cpi.htm>. Published roughly a year
  ahead. An unauthenticated fetch from this session returned HTTP 403 with no custom headers, which
  means the ingestion code needs a browser-like User-Agent or a different source — flagged here so
  the ingestion ticket does not rediscover it from scratch.
- BLS Employment Situation schedule: <https://www.bls.gov/schedule/news_release/empsit.htm>. Same
  publication pattern and the same fetch caveat as CPI.
- ALFRED release-dates API (<https://alfred.stlouisfed.org/help/downloaddata>) as a structured
  fallback: it returns actual historical release dates as JSON/XML per release ID, which sidesteps
  scraping BLS/Fed HTML for back-history. Release IDs still need to be confirmed against the
  headline (not research) CPI series and against the Employment Situation series before use.

## Rejected

- **Fixed UTC offset (e.g. always UTC-5).** Wrong for roughly half the days in the sample; rejected
  because the error is silent rather than a crash, which is the failure mode this decision exists to
  prevent.
- **Scraping BLS/Fed HTML as the only source.** Kept as the primary source because it is the
  authoritative one, but ALFRED is recorded as a fallback because the BLS schedule page already
  blocked one unauthenticated fetch during this research.

## Consequences

Irregular cases the calendar loader must handle, not silently normalize away:

- **Holiday moves.** Both BLS and the Fed publish the already-adjusted date; the loader takes the
  published date as-is and does no independent holiday arithmetic.
- **FOMC statements not at 14:00.** Intermeeting/emergency actions are not on the regular calendar
  page and do not follow the 14:00 convention — for example the COVID-era cuts released 2020-03-03
  at 10:00 EST and 2020-03-15 at 17:00 EDT. These are out of scope: the project measures reaction to
  *scheduled* releases, and an intermeeting action is by definition not scheduled. The loader must
  not pull these in if a future version scrapes a broader event list.
- **Ambiguous or missing dates.** A federal government shutdown can move a release date entirely
  (September 2025 CPI moved from 2025-10-15 to 2025-10-24) or cancel one (no Employment Situation
  report for the October 2025 reference month). The loader takes the realized date as published at
  the time, not a projected one, and a canceled release produces a missing row, not an imputed one —
  consistent with this project's stance that a null result is kept, not papered over.

Tests this convention implies, to be written with the calendar loader itself: a known EST date
converts to UTC-5, a known EDT date converts to UTC-4, and a release date adjacent to a DST
transition converts using the offset in effect on that date, not the offset in effect when the code
runs.

This decision does not select which specific releases go into the sample, or build the loader — that
is ingestion work for a follow-up ticket. It only fixes the convention and the sources so that ticket
does not have to re-derive them.

The open question above — which ALFRED series identify the headline CPI and Employment Situation
releases — is resolved in ADR 0003 (#17): the vintage dates of `CPIAUCNS` and `PAYNSA`.
