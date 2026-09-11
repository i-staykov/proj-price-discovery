"""Cache checksum-verified daily klines from data.binance.vision.

Verified bytes reach the final path through an atomic rename, so an interrupted write
cannot become a trusted cache entry. The preregistered sample uses 1-second klines.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import urllib.request
from datetime import date
from pathlib import Path
from urllib.error import HTTPError

from pricediscovery.calendar import load

_CACHE = Path(__file__).resolve().parents[2] / "data"
_MANIFEST = Path(__file__).with_name("data_manifest.csv")

_INTERVAL = "1s"

_ARCHIVE = (
    "https://data.binance.vision/data/spot/daily/klines"
    "/{symbol}/{interval}/{symbol}-{interval}-{day}.zip"
)


class ChecksumMismatch(Exception):
    def __init__(self, name: str, expected: str, actual: str):
        self.expected = expected
        super().__init__(f"{name}: expected {expected}, got {actual}")


def _download(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as resp:
        return resp.read()


def archive_path(day: date, symbol: str = "BTCUSDT", cache_dir: Path = _CACHE) -> Path:
    name = f"{symbol}-{_INTERVAL}-{day.isoformat()}.zip"
    return cache_dir / symbol / _INTERVAL / name


def daily_klines(day: date, symbol: str = "BTCUSDT", cache_dir: Path = _CACHE) -> Path:
    cached = archive_path(day, symbol, cache_dir)
    if cached.exists():
        return cached

    url = _ARCHIVE.format(symbol=symbol, interval=_INTERVAL, day=day.isoformat())
    archive = _download(url)
    expected = _download(url + ".CHECKSUM").decode().split()[0]
    actual = hashlib.sha256(archive).hexdigest()
    if actual != expected:
        raise ChecksumMismatch(cached.name, expected, actual)

    cached.parent.mkdir(parents=True, exist_ok=True)
    staging = cached.with_suffix(".zip.part")
    staging.write_bytes(archive)
    os.replace(staging, cached)
    return cached


def _manifest_rows(manifest: Path) -> dict[str, dict[str, str]]:
    if not manifest.exists():
        return {}
    with manifest.open(newline="") as stream:
        return {row["date"]: row for row in csv.DictReader(stream)}


def verify_cache(cache_dir: Path = _CACHE, manifest: Path = _MANIFEST) -> None:
    for row in _manifest_rows(manifest).values():
        cached = archive_path(date.fromisoformat(row["date"]), cache_dir=cache_dir)
        if row["status"] != "ok" or not cached.exists():
            continue
        actual = hashlib.sha256(cached.read_bytes()).hexdigest()
        if actual != row["sha256"]:
            raise ChecksumMismatch(cached.name, row["sha256"], actual)


def fetch_sample(retry: bool = False, cache_dir: Path = _CACHE, manifest: Path = _MANIFEST) -> None:
    verify_cache(cache_dir, manifest)
    rows = _manifest_rows(manifest)
    for day in sorted({release.date for release in load()}):
        key = day.isoformat()
        previous = rows.get(key)
        cached = archive_path(day, cache_dir=cache_dir)
        pinned = previous is not None and previous["status"] == "ok"
        if previous is not None and ((pinned and cached.exists()) or (not pinned and not retry)):
            continue
        expected = ""
        try:
            daily_klines(day, cache_dir=cache_dir)
            url = _ARCHIVE.format(symbol="BTCUSDT", interval=_INTERVAL, day=key)
            expected = _download(url + ".CHECKSUM").decode().split()[0]
            actual = hashlib.sha256(cached.read_bytes()).hexdigest()
            if actual != expected:
                raise ChecksumMismatch(cached.name, expected, actual)
            if pinned and actual != previous["sha256"]:
                raise ChecksumMismatch(cached.name, previous["sha256"], actual)
            outcome = "ok"
        except HTTPError as error:
            if error.code != 404 or pinned:
                raise
            outcome = "missing"
            expected = ""
        except ChecksumMismatch as error:
            cached.unlink(missing_ok=True)
            if pinned:
                raise
            outcome = "checksum_failed"
            expected = error.expected
        if pinned:
            continue
        rows[key] = {"date": key, "sha256": expected, "status": outcome}
        manifest.parent.mkdir(parents=True, exist_ok=True)
        staging = manifest.with_suffix(".csv.part")
        with staging.open("w", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=("date", "sha256", "status"))
            writer.writeheader()
            writer.writerows(rows.values())
        os.replace(staging, manifest)
        print(f"{key}: {outcome}", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch checksum-verified release-day archives.")
    parser.add_argument("--retry", action="store_true", help="Retry missing or failed days.")
    fetch_sample(retry=parser.parse_args().retry)
