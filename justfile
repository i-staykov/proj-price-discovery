default:
    @just --list

setup:
    uv sync --extra dev

lint:
    uv run ruff check .
    uv run ruff format --check .

fmt:
    uv run ruff format .

test:
    uv run pytest

check: lint test

# Rebuilds the release calendar snapshot from ALFRED and the Fed meeting calendars.
# Needs FRED_API_KEY in the environment. Run by hand: it hits api.stlouisfed.org and
# federalreserve.gov, neither of which CI reaches, so the snapshot is a committed
# artifact and only `load` is exercised by the tests.
calendar:
    uv run python -m pricediscovery.calendar

# Regenerates every figure and every number quoted in the README from raw data.
# Nothing may be typed into the README by hand.
results:
    @echo "No results yet. The estimand is undecided; see the Scoping milestone." && exit 1
