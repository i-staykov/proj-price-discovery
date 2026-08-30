import hashlib
from datetime import date

import pytest

from pricediscovery import ingest
from pricediscovery.ingest import ChecksumMismatch, daily_klines

DAY = date(2024, 6, 1)


@pytest.fixture
def archive() -> bytes:
    return b"the bytes the checksum is taken over; not a real zip"


@pytest.fixture
def responder(monkeypatch, archive):
    def install(checksum_hex: str) -> None:
        def fake(url: str) -> bytes:
            if url.endswith(".zip"):
                return archive
            return f"{checksum_hex}  archive.zip\n".encode()

        monkeypatch.setattr(ingest, "_download", fake)

    return install


def test_checksum_mismatch_raises_and_caches_nothing(tmp_path, responder):
    responder("0" * 64)
    with pytest.raises(ChecksumMismatch):
        daily_klines(DAY, cache_dir=tmp_path)
    assert list(tmp_path.rglob("*.zip")) == []


def test_verified_archive_is_written_to_the_cache(tmp_path, responder, archive):
    responder(hashlib.sha256(archive).hexdigest())
    path = daily_klines(DAY, cache_dir=tmp_path)
    assert path == tmp_path / "BTCUSDT" / "1s" / f"BTCUSDT-1s-{DAY.isoformat()}.zip"
    assert path.read_bytes() == archive
    assert list(tmp_path.rglob("*.part")) == []


def test_cached_day_is_not_refetched(tmp_path, monkeypatch, archive):
    cached = tmp_path / "BTCUSDT" / "1s" / f"BTCUSDT-1s-{DAY.isoformat()}.zip"
    cached.parent.mkdir(parents=True)
    cached.write_bytes(archive)

    def forbidden(url: str) -> bytes:
        raise AssertionError(f"network hit for {url}")

    monkeypatch.setattr(ingest, "_download", forbidden)
    assert daily_klines(DAY, cache_dir=tmp_path) == cached
