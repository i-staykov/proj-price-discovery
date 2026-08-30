import zipfile
from datetime import UTC, date, datetime

import pytest

from pricediscovery.align import event_window
from pricediscovery.calendar import to_utc

BASELINE = 100.0
SPIKE = BASELINE * 2.718281828459045  # e * baseline: log return of exactly 1.0


def _row(open_time_ms: int, close: float) -> list[str]:
    return [
        str(open_time_ms),
        f"{close}",
        f"{close}",
        f"{close}",
        f"{close}",
        "1",
        str(open_time_ms + 999),
        "1",
        "1",
        "0",
        "0",
        "0",
    ]


def _write_klines_zip(path, prices: dict[int, float]) -> None:
    rows = [_row(open_time_ms, close) for open_time_ms, close in sorted(prices.items())]
    body = "\n".join(",".join(row) for row in rows)
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("klines.csv", body)


def _spiky_day(tmp_path, release: datetime, present: range) -> None:
    release_ms = round(release.timestamp() * 1000)
    prices = {release_ms + s * 1000: BASELINE for s in present}
    prices[release_ms] = SPIKE
    path = tmp_path / "day.zip"
    _write_klines_zip(path, prices)
    return path


@pytest.fixture
def release() -> datetime:
    return datetime(2024, 6, 12, 12, 30, 0, tzinfo=UTC)


def test_jump_lands_at_tau_zero_not_adjacent(tmp_path, release):
    path = _spiky_day(tmp_path, release, range(-5, 6))
    result = event_window(release, path, window=(-5, 5))
    assert result[-1] == pytest.approx(0.0)
    assert result[0] == pytest.approx(1.0)
    assert result[1] == pytest.approx(0.0)


def test_missing_second_is_absent_not_forward_filled(tmp_path, release):
    present = [s for s in range(-5, 6) if s != 2]
    release_ms = round(release.timestamp() * 1000)
    prices = {release_ms + s * 1000: BASELINE for s in present}
    prices[release_ms] = SPIKE
    path = tmp_path / "day.zip"
    _write_klines_zip(path, prices)

    result = event_window(release, path, window=(-5, 5))
    assert 2 not in result
    assert set(result) == set(present)


def test_window_bounds_are_inclusive_and_exclude_outside(tmp_path, release):
    path = _spiky_day(tmp_path, release, range(-10, 11))
    result = event_window(release, path, window=(-5, 5))
    assert set(result) == set(range(-5, 6))


def test_raises_when_no_trade_precedes_release(tmp_path, release):
    release_ms = round(release.timestamp() * 1000)
    prices = {release_ms + s * 1000: BASELINE for s in range(0, 6)}
    path = tmp_path / "day.zip"
    _write_klines_zip(path, prices)

    with pytest.raises(ValueError):
        event_window(release, path, window=(-5, 5))


@pytest.mark.parametrize(
    "day",
    [date(2021, 3, 12), date(2021, 3, 15)],  # either side of the 2021 DST transition
)
def test_dst_boundary_release_aligns_to_tau_zero(tmp_path, day):
    release = to_utc(day, "CPI")
    path = _spiky_day(tmp_path, release, range(-5, 6))
    result = event_window(release, path, window=(-5, 5))
    assert result[0] == pytest.approx(1.0)
    assert result[-1] == pytest.approx(0.0)
    assert result[1] == pytest.approx(0.0)
