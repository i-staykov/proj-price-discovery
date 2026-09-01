"""Cache checksum-verified daily klines from data.binance.vision.

Verified bytes reach the final path through an atomic rename, so an interrupted write
cannot become a trusted cache entry. The preregistered sample uses 1-second klines.
"""

from __future__ import annotations

import hashlib
import os
import urllib.request
from datetime import date
from pathlib import Path

_CACHE = Path(__file__).resolve().parents[2] / "data"

_INTERVAL = "1s"

_ARCHIVE = (
    "https://data.binance.vision/data/spot/daily/klines"
    "/{symbol}/{interval}/{symbol}-{interval}-{day}.zip"
)


class ChecksumMismatch(Exception):
    pass


def _download(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as resp:
        return resp.read()


def daily_klines(day: date, symbol: str = "BTCUSDT", cache_dir: Path = _CACHE) -> Path:
    name = f"{symbol}-{_INTERVAL}-{day.isoformat()}.zip"
    cached = cache_dir / symbol / _INTERVAL / name
    if cached.exists():
        return cached

    url = _ARCHIVE.format(symbol=symbol, interval=_INTERVAL, day=day.isoformat())
    archive = _download(url)
    expected = _download(url + ".CHECKSUM").decode().split()[0]
    actual = hashlib.sha256(archive).hexdigest()
    if actual != expected:
        raise ChecksumMismatch(f"{name}: expected {expected}, got {actual}")

    cached.parent.mkdir(parents=True, exist_ok=True)
    staging = cached.with_suffix(".zip.part")
    staging.write_bytes(archive)
    os.replace(staging, cached)
    return cached
