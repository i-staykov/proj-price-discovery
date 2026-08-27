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

# model.pdf is committed; its source is not. Rebuilding requires docs/model/model.tex,
# which only exists in the author's working tree. See #21.
model:
    cd docs/model && pdflatex -interaction=nonstopmode -halt-on-error model.tex
    cd docs/model && pdflatex -interaction=nonstopmode -halt-on-error model.tex
    cp docs/model/model.pdf model.pdf

# Regenerates every figure and every number quoted in the README from raw data.
# Nothing may be typed into the README by hand.
results:
    @echo "No results yet. The estimand is undecided; see the Scoping milestone." && exit 1
