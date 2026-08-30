"""Daily kline archives from data.binance.vision, cached under data/.

Binance publishes one zip per symbol-day at a stable URL with a `.CHECKSUM` sidecar
holding the sha256 of the zip. `daily_klines` fetches a day once, checks it against
that sidecar, and writes it under data/; a later call for the same day reads the
cached file and never touches the network. A mismatch raises and nothing is
written, so a corrupted download is never cached and never silently retried.

1-second klines are the chosen product (ADR 0003, #7): second-level timing at a
fraction of the size of the trade-level archives.
"""

from __future__ import annotations

import hashlib
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
    cached.write_bytes(archive)
    return cached
