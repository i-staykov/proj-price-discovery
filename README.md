# proj-price-discovery

**How fast does the market incorporate new public information?**

Scheduled US macro releases (CPI and the Employment Situation at 08:30 ET, FOMC statements at
14:00 ET) arrive at a known second and are not caused by the market. That makes them a clean
instrument for measuring the speed of price discovery rather than its direction. Prices come from
`data.binance.vision`, which is free and requires no API key, and crypto trades continuously, so a
release lands in an open market with no session boundary to model.

This is a measurement study, not a trading strategy. There is no backtest here and there will not be
one.

## Status

🚧 **Scoping.** We are verifying the premise and have not chosen an estimand. Nothing in this
repository is a result yet.

The first question is whether crypto prices visibly react to US macro releases at all. If they do
not, the premise is wrong and the project changes or stops; that answer will be recorded here either
way. No estimation code will be written before `PREREGISTRATION.md` is merged, so that the plan
provably predates the results.

## Running it

Requires [uv](https://docs.astral.sh/uv/) and [just](https://github.com/casey/just); on macOS,
`brew install uv just`. Python is pinned to 3.12 or newer by `pyproject.toml` and installed by uv.

```sh
just setup   # uv sync, creates .venv from pyproject.toml and uv.lock
just check   # ruff and pytest
```

Dependencies live in `pyproject.toml` and are pinned in `uv.lock`. There is no `requirements.txt`
on purpose: one manifest, one lockfile, no third place to drift. `just setup` installs the `dev`
extra; the `notebook` extra adds pandas, matplotlib, requests and a kernel for `notebooks/`, via
`uv sync --extra notebook`.

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
- `model.pdf` — the model in fifteen slides, for a reader meeting it for the first time. Source in
  `docs/model/`.
- `docs/framings/` — the estimand and the model, stated rather than explained. `docs/adr/` — one
  short record per decision that is expensive to reverse. `docs/limitations.md` — the objections,
  including those with no answer.
- `src/pricediscovery/` — library code. `tests/` — tests, in particular for event-time alignment.

## Licence

MIT, see `LICENSE`.
