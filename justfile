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

# Regenerates every figure and every number quoted in the README from raw data.
# Nothing may be typed into the README by hand.
results:
    @echo "No results yet. The estimand is undecided; see the Scoping milestone." && exit 1
