"""Daily kline archives from data.binance.vision, cached under data/.

Binance publishes one zip per symbol-day at a stable URL with a `.CHECKSUM` sidecar
holding the sha256 of the zip. `daily_klines` fetches a day once, checks it against
that sidecar, and writes it under data/; a later call for the same day reads the
cached file and never touches the network. A mismatch raises and nothing is
written, and the verified bytes reach their final path through an atomic rename,
so a cached entry is always either absent or the checked archive.

1-second klines are the chosen product: the preregistered sample (PREREGISTRATION.md
"Sample") and the notation (docs/framings/notation.md) both rest on #7's
recommendation of second-level klines over the trade-level archives.
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
