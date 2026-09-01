# 0001 Release timezone convention

Status: accepted
Date: 2026-08-25
Issue: #8

## Context

CPI, the Employment Situation and FOMC statements are scheduled in US Eastern local time; prices
are indexed in UTC. Eastern switches between UTC-5 and UTC-4. A naive timestamp or fixed offset
silently misaligns half the sample by an hour.

## Decision

Release times are stored as local wall-clock time in the `America/New_York` IANA zone and converted
to UTC at load time via the IANA tz database (`zoneinfo`/`pandas`), never with a fixed offset. The
conversion happens once, in the calendar-loading step, so every downstream consumer works in UTC only.

Scheduled times:

- CPI and the Employment Situation: 08:30 ET.
- FOMC statements, regularly scheduled meetings only: 14:00 ET, in effect since March 2013.

Calendar sources are fixed in ADR 0003.

## Rejected

- **Fixed UTC offset.** Wrong for roughly half the sample and silent.

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
  the time, not a projected one, and a canceled release produces no row.

Tests pin one EST date, one EDT date and a date on each side of a DST transition.
