from collections import Counter
from datetime import UTC, date, datetime, timedelta

from pricediscovery.calendar import (
    PRIMARY_SAMPLE,
    SAMPLE_END,
    SAMPLE_START,
    load,
    to_utc,
)


def test_no_naive_timestamp_survives_the_loader():
    for release in load():
        assert release.timestamp_utc.tzinfo is not None
        assert release.timestamp_utc.utcoffset() == timedelta(0)


def test_est_release_converts_at_utc_minus_5():
    # CPI, 08:30 ET, mid-January: America/New_York is UTC-5.
    assert to_utc(date(2019, 1, 11), "CPI") == datetime(2019, 1, 11, 13, 30, tzinfo=UTC)


def test_edt_release_converts_at_utc_minus_4():
    # CPI, 08:30 ET, mid-June: America/New_York is UTC-4.
    assert to_utc(date(2019, 6, 12), "CPI") == datetime(2019, 6, 12, 12, 30, tzinfo=UTC)


def test_conversion_uses_the_offset_in_effect_on_the_release_date():
    # DST began 2021-03-14. The offset must switch across that date, not track "now".
    assert to_utc(date(2021, 3, 12), "CPI").hour == 13  # still EST
    assert to_utc(date(2021, 3, 15), "CPI").hour == 12  # EDT


def test_fomc_uses_the_1400_eastern_convention():
    assert to_utc(date(2024, 1, 31), "FOMC") == datetime(2024, 1, 31, 19, 0, tzinfo=UTC)  # EST


def test_known_cpi_release_lands_at_0830_eastern():
    calendar = {(r.release_type, r.date): r for r in load()}
    cpi = calendar[("CPI", date(2024, 11, 13))]
    assert cpi.timestamp_utc == datetime(2024, 11, 13, 13, 30, tzinfo=UTC)


def test_calendar_is_sorted_and_within_the_sample_window():
    calendar = load()
    assert calendar == sorted(calendar, key=lambda r: (r.timestamp_utc, r.release_type))
    assert all(SAMPLE_START <= r.date <= SAMPLE_END for r in calendar)
    assert {r.release_type for r in calendar} == {"CPI", "EmploymentSituation", "FOMC"}


def test_primary_sample_counts_match_the_realised_schedule():
    counts = Counter(r.release_type for r in load())
    # 107 calendar months in the window; one CPI and one Employment Situation release
    # each, minus the two 2025 shutdown cancellations.
    assert counts["CPI"] == 106
    assert counts["EmploymentSituation"] == 106


def test_shutdown_cancellations_are_absent_not_imputed():
    days = {(r.release_type, r.date.year, r.date.month) for r in load()}
    # No Employment Situation for the October 2025 reference month; no CPI released in
    # November 2025. Federal shutdown (ADR 0001). The rows are simply missing.
    assert ("EmploymentSituation", 2025, 10) not in days
    assert ("CPI", 2025, 11) not in days

    per_month = Counter((r.release_type, r.date.year, r.date.month) for r in load())
    assert per_month.most_common(1)[0][1] == 1  # never two of the same release in one month


def test_fomc_is_loaded_but_not_in_the_primary_sample():
    counts = Counter(r.release_type for r in load())
    assert counts["FOMC"] == 71
    assert "FOMC" not in PRIMARY_SAMPLE


def test_every_row_records_a_checkable_source():
    for r in load():
        assert r.source.startswith(
            ("https://alfred.stlouisfed.org/", "https://www.federalreserve.gov/")
        )
