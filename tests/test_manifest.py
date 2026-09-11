import csv
import hashlib
import re
from datetime import date
from types import SimpleNamespace
from urllib.error import HTTPError

import pytest

from pricediscovery import ingest
from pricediscovery.calendar import load

DAY = date(2024, 6, 12)
ARCHIVE = b"checksum fixture"
DIGEST = hashlib.sha256(ARCHIVE).hexdigest()


def write_manifest(manifest, status="ok", digest=DIGEST):
    manifest.write_text(f"date,sha256,status\n{DAY},{digest},{status}\n")


@pytest.fixture
def sample(tmp_path, monkeypatch):
    monkeypatch.setattr(ingest, "load", lambda: [SimpleNamespace(date=DAY)])
    return tmp_path / "cache", tmp_path / "manifest.csv"


def test_manifest_covers_each_calendar_date_once():
    with ingest._MANIFEST.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    days = {release.date.isoformat() for release in load()}
    assert len(rows) == len(days) == 279
    assert {row["date"] for row in rows} == days
    for row in rows:
        assert row["status"] in {"ok", "missing", "checksum_failed"}
        if row["status"] == "missing":
            assert row["sha256"] == ""
        else:
            assert re.fullmatch(r"[0-9a-f]{64}", row["sha256"])


def test_verify_cache_detects_an_altered_byte(sample):
    cache, manifest = sample
    write_manifest(manifest)
    cached = ingest.archive_path(DAY, cache_dir=cache)
    cached.parent.mkdir(parents=True)
    cached.write_bytes(ARCHIVE + b"x")
    with pytest.raises(ingest.ChecksumMismatch):
        ingest.verify_cache(cache, manifest)


def test_verify_cache_allows_an_absent_archive(sample):
    cache, manifest = sample
    write_manifest(manifest)
    ingest.verify_cache(cache, manifest)


@pytest.mark.parametrize("cached_first", [False, True])
def test_new_days_verified_and_full_cache_offline(sample, monkeypatch, cached_first):
    cache, manifest = sample
    calls = []

    def download(url):
        calls.append(url)
        return DIGEST.encode() if url.endswith(".CHECKSUM") else ARCHIVE

    monkeypatch.setattr(ingest, "_download", download)
    cached = ingest.archive_path(DAY, cache_dir=cache)
    if cached_first:
        cached.parent.mkdir(parents=True)
        cached.write_bytes(ARCHIVE)
    ingest.fetch_sample(cache_dir=cache, manifest=manifest)
    assert any(url.endswith(".CHECKSUM") for url in calls)
    assert sum(url.endswith(".zip") for url in calls) == int(not cached_first)
    recorded = manifest.read_bytes()
    calls.clear()
    ingest.fetch_sample(cache_dir=cache, manifest=manifest)
    assert calls == []
    assert manifest.read_bytes() == recorded


def test_retry_replaces_missing_row_in_place(sample, monkeypatch):
    cache, manifest = sample
    write_manifest(manifest, status="missing", digest="")
    original = manifest.read_bytes()

    def download(url):
        return DIGEST.encode() if url.endswith(".CHECKSUM") else ARCHIVE

    monkeypatch.setattr(ingest, "_download", download)
    ingest.fetch_sample(cache_dir=cache, manifest=manifest)
    assert manifest.read_bytes() == original
    assert not cache.exists()
    ingest.fetch_sample(retry=True, cache_dir=cache, manifest=manifest)
    with manifest.open() as stream:
        rows = list(csv.DictReader(stream))
    assert rows == [{"date": str(DAY), "sha256": DIGEST, "status": "ok"}]


@pytest.mark.parametrize("code", [404, 503])
def test_only_new_404_is_recorded_as_missing(sample, monkeypatch, code):
    cache, manifest = sample

    def fail(url):
        raise HTTPError(url, code, "fixture", {}, None)

    monkeypatch.setattr(ingest, "_download", fail)
    if code == 404:
        ingest.fetch_sample(cache_dir=cache, manifest=manifest)
        assert ",,missing" in manifest.read_text()
    else:
        with pytest.raises(HTTPError):
            ingest.fetch_sample(cache_dir=cache, manifest=manifest)
        assert not manifest.exists()


@pytest.mark.parametrize("cached_first", [False, True])
def test_checksum_failure_is_recorded_and_archive_removed(sample, monkeypatch, cached_first):
    cache, manifest = sample
    cached = ingest.archive_path(DAY, cache_dir=cache)
    if cached_first:
        cached.parent.mkdir(parents=True)
        cached.write_bytes(ARCHIVE)
    monkeypatch.setattr(
        ingest, "_download", lambda url: b"0" * 64 if url.endswith(".CHECKSUM") else ARCHIVE
    )
    ingest.fetch_sample(cache_dir=cache, manifest=manifest)
    assert ",checksum_failed" in manifest.read_text()
    assert not cached.exists()


@pytest.mark.parametrize("response", ["same", "changed", "missing"])
def test_refetch_never_changes_a_pinned_manifest(sample, monkeypatch, response):
    cache, manifest = sample
    write_manifest(manifest)
    recorded = manifest.read_bytes()
    archive = ARCHIVE if response == "same" else b"changed upstream"

    def download(url):
        if response == "missing":
            raise HTTPError(url, 404, "fixture", {}, None)
        digest = hashlib.sha256(archive).hexdigest().encode()
        return digest if url.endswith(".CHECKSUM") else archive

    monkeypatch.setattr(ingest, "_download", download)
    if response == "same":
        ingest.fetch_sample(cache_dir=cache, manifest=manifest)
        assert ingest.archive_path(DAY, cache_dir=cache).read_bytes() == ARCHIVE
    else:
        error = HTTPError if response == "missing" else ingest.ChecksumMismatch
        with pytest.raises(error):
            ingest.fetch_sample(cache_dir=cache, manifest=manifest)
    assert manifest.read_bytes() == recorded
