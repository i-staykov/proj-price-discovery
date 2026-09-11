import json

import numpy as np
import pytest

from pricediscovery.prior_predictive import RESULT, SEED, measure, terminal_returns


def test_seed_fixes_every_candidate_statistic():
    first = measure(seed=SEED, datasets=40, events=12)
    assert first == measure(seed=SEED, datasets=40, events=12)
    assert first != measure(seed=SEED + 1, datasets=40, events=12)


def test_preregistered_prior_exceedance_and_dataset_standard_error():
    result = measure()
    original = result["candidates"]["a"]
    assert result["datasets"] >= 2000
    assert result["events_per_dataset"] == 212
    assert 0.13 <= original["exceedance_500_bp"] <= 0.18
    absolute = np.abs(terminal_returns("a", SEED, 2000, 212))
    fractions = np.mean(absolute > 500, axis=1)
    assert original["exceedance_500_bp_se"] == pytest.approx(fractions.std(ddof=1) / np.sqrt(2000))
    assert original["exceedance_500_bp_se"] > np.sqrt(0.18 * 0.82 / absolute.size)


def test_hyperparameters_are_redrawn_per_dataset():
    # Shared volatility hyperparameters induce clustering in the event exceedance indicators.
    absolute = np.abs(terminal_returns("a", SEED, 2000, 212))
    fractions = np.mean(absolute > 500, axis=1)
    assert fractions.std() > 0.15


def test_committed_candidates_reproduce():
    expected = json.loads(RESULT.read_text())
    actual = measure()
    candidates = expected.pop("candidates")
    measured = actual.pop("candidates")
    assert actual == expected
    for candidate, summary in candidates.items():
        for quantity, value in summary.items():
            if isinstance(value, str):
                assert measured[candidate][quantity] == value
            else:
                # Transcendental functions can round differently across CPU libraries.
                assert measured[candidate][quantity] == pytest.approx(value, rel=1e-12)
