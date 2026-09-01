# proj-price-discovery

**How fast does the market incorporate new public information?**

The primary events are CPI and Employment Situation releases at 08:30 ET. FOMC statements at
14:00 ET are a robustness sample because the chair's 14:30 press conference contaminates the
one-hour window. BTCUSDT prices come from `data.binance.vision`; crypto trades continuously, so a
release lands in an open market with no session boundary to model.

This is a measurement study, not a trading strategy.

## Status

**Pipeline complete.** The premise passed its kill-check, the analysis is preregistered, and the
calendar, ingestion and alignment layers are tested. Estimation has not started.

## Running it

Requires [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just); on macOS,
`brew install uv just`. Python is pinned to 3.12 or newer by `pyproject.toml` and installed by uv.

```sh
just setup   # uv sync, creates .venv from pyproject.toml and uv.lock
just check   # ruff and pytest
```

Dependencies live in `pyproject.toml` and are pinned in `uv.lock`. `just setup` installs the `dev`
extra. For notebooks: `uv sync --extra notebook`.

`model.pdf` needs a LaTeX distribution with beamer, TikZ and pgfplots, which TeX Live and MacTeX
both provide. It is committed, so this is only needed to change it:

```sh
cd docs/model && pdflatex model.tex && cp model.pdf ../../model.pdf
```

`just results` will regenerate every figure and every number quoted in this README from raw data. It
currently exits non-zero, because there are no results to regenerate.

## How the repository is organised

- `CLAUDE.md` — the standing rules: what the project is, what may not be done, and the writing
  standard reviews enforce.
- `CONTRIBUTING.md` — the ticket-to-merge workflow.
- `model.pdf` — the model deck. Source in `docs/model/`.
- `docs/framings/` — the estimand and the model.
- `docs/adr/` — one short record per decision that is expensive to reverse.
- `docs/limitations.md` — the objections.
- `src/pricediscovery/` — library code. `tests/` — tests, in particular for event-time alignment.
