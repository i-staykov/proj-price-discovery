# 0003 Release calendar sources: ALFRED vintage dates and the Fed meeting calendars

Status: accepted
Date: 2026-08-30
Issue: #24 (built in #17)

## Context

ADR 0001 fixed the timezone convention and named the ALFRED release-dates API as the structured
fallback to the BLS schedule pages, but left one thing open: "Release IDs still need to be confirmed
against the headline (not research) CPI series and against the Employment Situation series before
use." Building the loader in #17 forces that choice, and the same choice for FOMC.

An unauthenticated BLS fetch returned HTTP 403 again, as ADR 0001 predicted, so ALFRED carries the
two BLS releases.

## Decision

CPI and Employment Situation release dates are the **ALFRED vintage dates of the
non-seasonally-adjusted headline series**, `CPIAUCNS` and `PAYNSA`, read from `api.stlouisfed.org`
with a FRED API key. A vintage date is the day a value was first published, which for these series
is the BLS release day; the nine CPI dates used in the #6 kill-check all reproduce exactly.

FOMC statement dates are parsed from the **Federal Reserve meeting calendars** — `fomccalendars.htm`
for the years it still lists, `fomchistorical{year}.htm` before that, with the boundary read off the
current page rather than hardcoded. The statement date comes from the `monetaryYYYYMMDDa` link in a
meeting row; a row counts as a regularly scheduled meeting if its date label carries a two-day range
and it produced a statement. This keeps the 14:00 ET scheduled statements and drops intermeeting
actions, notation votes and framework statements.

`load` reads a committed snapshot. The fetch is a separate `refresh` step run by hand (`just
calendar`), so the network is touched only on a deliberate rebuild and CI stays offline.

## Rejected

**Seasonally adjusted series (`CPIAUCSL`, `PAYEMS`).** Their vintage histories carry extra entries
from the annual re-estimation of seasonal factors — six spurious February dates for `CPIAUCSL` in
the window — which are revisions, not releases.

**The `fred/release/dates` endpoint (release IDs 10 and 50).** Returns several dates per month for
the same reason: annual revision publications listed alongside the headline print.

**Scraping the BLS schedule pages.** Blocked, and they only reach about a year back.

**A live Fed-calendar parser inside `load`.** The calendar changes eight times a year; a committed
snapshot with a manual refresh keeps `load` and the tests deterministic and offline.

## Consequences

The realised primary sample is **212 events, not the 214** estimated from publication cadence before
verification: the 2025 federal shutdown left no CPI release in November 2025 and cancelled the
October 2025 Employment Situation (ADR 0001). Both are absent from the calendar, not imputed. FOMC
contributes **71** scheduled statements. The deviation is logged in `PREREGISTRATION.md`.

`refresh` depends on `api.stlouisfed.org` and `federalreserve.gov`, which CI cannot reach and does
not exercise. A structural change to either page — the Fed dropping its `YYYY FOMC Meetings`
headings, ALFRED renaming the vintage field — fails the next manual rebuild loudly rather than
producing a wrong snapshot.

The open release-ID question in ADR 0001 is resolved.
