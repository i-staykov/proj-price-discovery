"""Event-time alignment: R(tau) for one release from one daily kline archive.

`event_window` reads a `daily_klines` archive (#18) and returns the cumulative log
return from the last traded price strictly before the release, indexed by whole
seconds relative to the release instant (notation in docs/framings/notation.md).
Both inputs are UTC; the release calendar (#8) already carries the DST-correct
offset, so alignment here is integer second arithmetic on two UTC instants, never
a timezone lookup. A one-second or one-hour slip here would produce a clean null
rather than an error, so this is the pipeline's dominant error risk (#19).

Seconds with no trade have no row in the archive and are absent from the result,
never forward-filled: `tau in window` is how a caller distinguishes a flat second
from a missing one.
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


def _seconds(klines_zip: Path) -> list[tuple[int, float]]:
    with zipfile.ZipFile(klines_zip) as zf:
        raw = zf.read(zf.namelist()[0]).decode()
    return sorted(
        (int(row[_OPEN_TIME]), float(row[_CLOSE])) for row in csv.reader(io.StringIO(raw))
    )


def event_window(
    release_utc: datetime,
    klines_zip: Path,
    window: tuple[int, int] = (-300, 3600),
) -> dict[int, float]:
    """R(tau) = log P(tau) - log P(0-) for every traded second tau in `window`.

    P(0-) is the close of the last traded second strictly before `release_utc`.
    Raises ValueError if no trade precedes the release.
    """
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
