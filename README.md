# proj-price-discovery

**How fast does the market incorporate new public information?**

The primary events are CPI and Employment Situation releases at 08:30 ET. FOMC statements at
14:00 ET are a robustness sample because the chair's 14:30 press conference contaminates the
one-hour window. BTCUSDT prices come from `data.binance.vision`; crypto trades continuously, so a
release lands in an open market with no session boundary to model.

This is a measurement study, not a trading strategy.

## Status

The analysis is preregistered; calendar, ingestion and alignment code are tested.
Prior specification, concurrent-release screening and validation gates remain open. No primary fit
has run.

## Running it

Requires [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just); on macOS,
`brew install uv just`. Python is pinned to 3.12 or newer by `pyproject.toml` and installed by uv.

```sh
just setup   # uv sync, creates .venv from pyproject.toml and uv.lock
just check   # ruff and pytest
```

Dependencies live in `pyproject.toml` and are pinned in `uv.lock`. `just setup` installs the `dev`
extra. For notebooks: `uv sync --extra notebook`.

[The model presentation](model-explained.pdf) is committed. Rebuilding it requires a LaTeX distribution
with beamer, TikZ and pgfplots (TeX Live or MacTeX):

```sh
just model
```

`just results` will regenerate every figure and every number quoted in this README from raw data. It
currently exits non-zero, because there are no results to regenerate.

## How the repository is organised

- `CLAUDE.md`: standing rules and writing standard.
- `CONTRIBUTING.md`: issue and review workflow.
- `docs/model/model-explained.tex`: source for the single model presentation.
- `docs/framings/`: estimand and model.
- `docs/adr/`: decisions and rejected alternatives.
- `docs/limitations.md`: assumptions, objections and planned checks.
- `src/pricediscovery/` and `tests/`: library code and tests.
