"""Align one daily kline archive to a release instant.

Binance Spot timestamps switch from milliseconds to microseconds on 2025-01-01.
`tau` keys the kline opening second, not elapsed time; ADR 0004 maps horizons to
indices. Missing seconds remain absent.
"""

from __future__ import annotations

import csv
import io
import zipfile
from datetime import datetime
from math import log
from pathlib import Path

_OPEN_TIME = 0
_CLOSE = 4
_MICROSECONDS = 1_000_000_000_000_000


def _milliseconds(timestamp: int) -> int:
    return timestamp // 1000 if timestamp >= _MICROSECONDS else timestamp


def _seconds(klines_zip: Path) -> list[tuple[int, float]]:
    with zipfile.ZipFile(klines_zip) as zf:
        raw = zf.read(zf.namelist()[0]).decode()
    return sorted(
        (_milliseconds(int(row[_OPEN_TIME])), float(row[_CLOSE]))
        for row in csv.reader(io.StringIO(raw))
    )


def event_window(
    release_utc: datetime,
    klines_zip: Path,
    window: tuple[int, int] = (-300, 3600),
) -> dict[int, float]:
    """Return cumulative log returns keyed by kline opening second; see ADR 0004."""
    release_ms = round(release_utc.timestamp() * 1000)
    seconds = _seconds(klines_zip)

    before = [close for open_time_ms, close in seconds if open_time_ms < release_ms]
    if not before:
        raise ValueError(f"no trade before release {release_utc.isoformat()}")
    baseline = log(before[-1])

    lo, hi = window
    return {
        (open_time_ms - release_ms) // 1000: log(close) - baseline
        for open_time_ms, close in seconds
        if lo <= (open_time_ms - release_ms) // 1000 <= hi
    }
