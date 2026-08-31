import zipfile
from datetime import UTC, date, datetime
from math import log

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


def test_horizon_grid_maps_to_expected_indices(tmp_path, release):
    # ADR 0004: window[tau] is the kline covering [release+tau, release+tau+1s),
    # so a horizon of k seconds -- the move over [release, release+k s) -- is
    # read at index k-1, and the preregistered grid lands on {0, 9, 59, 599, 3599}.
    release_ms = round(release.timestamp() * 1000)
    prices = {release_ms + s * 1000: BASELINE + s for s in range(-1, 3600)}
    path = tmp_path / "day.zip"
    _write_klines_zip(path, prices)

    result = event_window(release, path)  # default window covers (-300, 3600)
    baseline = log(BASELINE - 1)  # P(0-) is the kline opening at tau = -1

    grid_seconds_to_index = {1: 0, 10: 9, 60: 59, 600: 599, 3600: 3599}
    for horizon_s, index in grid_seconds_to_index.items():
        assert index == horizon_s - 1
        assert result[index] == pytest.approx(log(BASELINE + index) - baseline)


@pytest.mark.parametrize(
    "day",
    [date(2021, 3, 12), date(2021, 3, 15)],  # either side of the 2021 DST transition
)
def test_alignment_has_no_timezone_dependence(tmp_path, day):
    # to_utc's DST correctness is test_calendar.py's job. This only shows align.py
    # does integer arithmetic on the UTC instant and never consults the ET offset:
    # the fixture is built from the same to_utc call, so a wrong offset would shift
    # fixture and alignment together and the jump would still sit at tau = 0.
    release = to_utc(day, "CPI")
    path = _spiky_day(tmp_path, release, range(-5, 6))
    result = event_window(release, path, window=(-5, 5))
    assert result[0] == pytest.approx(1.0)
    assert result[-1] == pytest.approx(0.0)
    assert result[1] == pytest.approx(0.0)
