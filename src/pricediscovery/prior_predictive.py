import argparse
import json
from pathlib import Path

import numpy as np

SEED = 4201
DATASETS = 2000
EVENTS = 212
RESULT = Path("results/prior_predictive_candidates.json")
CANDIDATES = {
    "a": (False, False),
    "b": (True, True),
    "c": (False, True),
    "d": (True, False),
}


def terminal_returns(candidate: str, seed: int, datasets: int, events: int) -> np.ndarray:
    student_magnitude, revised_volatility = CANDIDATES[candidate]
    # Separate streams keep unchanged components identical across candidate arms.
    magnitude_key, volatility_key, noise_key = np.random.SeedSequence(seed).spawn(3)
    magnitude_rng = np.random.default_rng(magnitude_key)
    volatility_rng = np.random.default_rng(volatility_key)
    noise_rng = np.random.default_rng(noise_key)
    shape = (datasets, events)
    if student_magnitude:
        magnitude = 200 * magnitude_rng.standard_t(4, size=shape)
    else:
        mu_m = magnitude_rng.normal(np.log(30), 1, size=(datasets, 1))
        sigma_m = np.abs(magnitude_rng.normal(size=(datasets, 1)))
        # Symmetric independent noise gives the same |R(H)| law for either sign of M.
        magnitude = np.exp(mu_m + sigma_m * magnitude_rng.normal(size=shape))
    nu_location, nu_scale = (np.log(1.2), 0.75) if revised_volatility else (0, 2)
    omega_scale = 0.75 if revised_volatility else 1
    nu = volatility_rng.normal(nu_location, nu_scale, size=(datasets, 1))
    omega = np.abs(volatility_rng.normal(0, omega_scale, size=(datasets, 1)))
    volatility = np.exp(nu + omega * volatility_rng.normal(size=shape))
    # At H the normalised mean is exactly M; rate priors do not enter this marginal.
    return magnitude + 60 * volatility * noise_rng.normal(size=shape)


def measure(seed: int = SEED, datasets: int = DATASETS, events: int = EVENTS) -> dict:
    results = {}
    for candidate, (student_magnitude, revised_volatility) in CANDIDATES.items():
        absolute = np.abs(terminal_returns(candidate, seed, datasets, events))
        summary = {
            "magnitude_prior": "StudentT(4, 0, 200)" if student_magnitude else "preregistered",
            "volatility_prior": "proposal_31" if revised_volatility else "preregistered",
            "p95_abs_return_bp": float(np.quantile(absolute, 0.95)),
            "p99_abs_return_bp": float(np.quantile(absolute, 0.99)),
        }
        for bound in (500, 1000):
            fractions = np.mean(absolute > bound, axis=1)
            fraction = float(np.mean(fractions))
            se = float(np.std(fractions, ddof=1) / np.sqrt(datasets))
            summary[f"exceedance_{bound}_bp"] = fraction
            summary[f"exceedance_{bound}_bp_se"] = se
            summary[f"exceedance_{bound}_bp_mc95"] = [
                max(0, fraction - 1.96 * se),
                min(1, fraction + 1.96 * se),
            ]
        results[candidate] = summary
    return {
        "seed": seed,
        "datasets": datasets,
        "events_per_dataset": events,
        "terminal_horizon_s": 3600,
        "return_unit": "bp log return",
        "uncertainty": "Monte Carlo standard errors across independent datasets, not events",
        "candidates": results,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Measure the four candidate prior sets for #42.")
    parser.add_argument("--output", type=Path, default=RESULT)
    output = parser.parse_args().output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(measure(), indent=2, allow_nan=False) + "\n")
