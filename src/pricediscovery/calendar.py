"""Scheduled US macro releases as UTC timestamps.

CPI and the Employment Situation form the primary sample; FOMC statements are loaded
for the robustness comparison only (ADR 0002). Release dates come from ALFRED vintage
dates and the Federal Reserve's meeting calendars (ADR 0001). `refresh` does the
fetching and rewrites `release_calendar.csv`; everything downstream reads that snapshot
through `load`, so the only network access is a deliberate refresh.

The snapshot stores the published local date; `load` attaches the scheduled Eastern
wall-clock time and converts to UTC through the IANA database, so the offset is the one
in effect on the release date rather than the one in effect when the code runs.
"""

from __future__ import annotations

import csv
import json
import os
import re
import urllib.request
from dataclasses import dataclass
from datetime import UTC, date, datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

_SNAPSHOT = Path(__file__).parent / "release_calendar.csv"

_EASTERN = ZoneInfo("America/New_York")

# Scheduled wall-clock release time in US Eastern (ADR 0001).
_RELEASE_TIME = {
    "CPI": time(8, 30),
    "EmploymentSituation": time(8, 30),
    "FOMC": time(14, 0),
}

PRIMARY_SAMPLE = ("CPI", "EmploymentSituation")

# BTCUSDT 1s klines are complete from 2017-09-01; the last archive month at
# preregistration is 2026-07 (#7, ADR 0002).
SAMPLE_START = date(2017, 9, 1)
SAMPLE_END = date(2026, 7, 31)


@dataclass(frozen=True)
class Release:
    release_type: str
    date: date
    timestamp_utc: datetime
    source: str


def to_utc(day: date, release_type: str) -> datetime:
    local = datetime.combine(day, _RELEASE_TIME[release_type], tzinfo=_EASTERN)
    return local.astimezone(UTC)


def load(path: Path = _SNAPSHOT) -> list[Release]:
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    calendar = [
        Release(
            release_type=row["release_type"],
            date=date.fromisoformat(row["date"]),
            timestamp_utc=to_utc(date.fromisoformat(row["date"]), row["release_type"]),
            source=row["source"],
        )
        for row in rows
    ]
    calendar.sort(key=lambda r: (r.timestamp_utc, r.release_type))
    return calendar


_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122 Safari/537.36"
)

_ALFRED_API = "https://api.stlouisfed.org/fred/series/vintagedates"
_ALFRED_PAGE = "https://alfred.stlouisfed.org/series?seid={series_id}"

# NSA headline series. Their ALFRED vintage dates are exactly the BLS release dates;
# the seasonally adjusted counterparts (CPIAUCSL, PAYEMS) carry extra vintages from
# annual re-seasonalisation that are not releases.
_SERIES = {"CPI": "CPIAUCNS", "EmploymentSituation": "PAYNSA"}

_FOMC_CURRENT = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
_FOMC_HISTORICAL = "https://www.federalreserve.gov/monetarypolicy/fomchistorical{year}.htm"

# fomccalendars.htm currently starts at 2021; earlier years need the historical pages.
_FOMC_CURRENT_FROM = 2021

# The statement PDF/HTML link carries the statement date: monetary20230201a.htm.
_STATEMENT_LINK = re.compile(r"monetary(\d{8})a\d?\.(?:htm|pdf)")


def _get(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(request, timeout=60) as resp:
        return resp.read().decode()


def _alfred_release_dates(series_id: str) -> list[date]:
    query = f"series_id={series_id}&limit=10000&file_type=json&api_key={os.environ['FRED_API_KEY']}"
    with urllib.request.urlopen(f"{_ALFRED_API}?{query}", timeout=60) as resp:
        payload = json.load(resp)
    return [date.fromisoformat(d) for d in payload["vintage_dates"]]


# A regularly scheduled meeting spans two consecutive days; the day cell reads "27-28".
# Single-day entries on these pages are notation votes, framework statements or
# intermeeting actions, none of which follow the 14:00 ET convention (ADR 0001).
_TWO_DAY = re.compile(r"\d{1,2}-\d{1,2}")
_NOT_A_MEETING = ("unscheduled", "cancelled", "notation vote")


def _fomc_current() -> list[date]:
    dates = []
    for row in _get(_FOMC_CURRENT).split("fomc-meeting__date")[1:]:
        label, _, body = row.partition("</div>")
        if _scheduled(label) and _STATEMENT_LINK.search(body):
            dates.append(_statement_date(body))
    return dates


def _fomc_historical(year: int) -> list[date]:
    dates = []
    for panel in re.split(r"<h5[^>]*>", _get(_FOMC_HISTORICAL.format(year=year)))[1:]:
        heading, _, body = panel.partition("</h5>")
        if "Meeting" in heading and _scheduled(heading) and _STATEMENT_LINK.search(body):
            dates.append(_statement_date(body))
    return dates


def _scheduled(text: str) -> bool:
    text = re.sub(r"<[^>]+>", "", text)
    return bool(_TWO_DAY.search(text)) and not any(mark in text for mark in _NOT_A_MEETING)


def _statement_date(html: str) -> date:
    return datetime.strptime(_STATEMENT_LINK.search(html).group(1), "%Y%m%d").date()


def refresh(path: Path = _SNAPSHOT) -> None:
    rows: list[tuple[str, date, str]] = []

    for release_type, series_id in _SERIES.items():
        source = _ALFRED_PAGE.format(series_id=series_id)
        rows += [
            (release_type, day, source)
            for day in _alfred_release_dates(series_id)
            if SAMPLE_START <= day <= SAMPLE_END
        ]

    fomc = [(day, _FOMC_CURRENT) for day in _fomc_current()]
    for year in range(SAMPLE_START.year, _FOMC_CURRENT_FROM):
        fomc += [(day, _FOMC_HISTORICAL.format(year=year)) for day in _fomc_historical(year)]
    rows += [("FOMC", day, source) for day, source in fomc if SAMPLE_START <= day <= SAMPLE_END]

    rows.sort(key=lambda r: (r[1], r[0]))
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["release_type", "date", "source"])
        for release_type, day, source in rows:
            writer.writerow([release_type, day.isoformat(), source])


if __name__ == "__main__":
    refresh()
    print(f"wrote {_SNAPSHOT}")
