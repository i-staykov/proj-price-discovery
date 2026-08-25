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

```sh
just setup   # uv sync, creates .venv
just check   # ruff and pytest
```

`just results` will regenerate every figure and every number quoted in this README from raw data. It
currently exits non-zero, because there are no results to regenerate.

## How the repository is organised

- `CLAUDE.md` — the standing rules: what the project is, what may not be done, and the writing
  standard reviews enforce.
- `CONTRIBUTING.md` — the ticket-to-merge workflow.
- `docs/adr/` — one short record per decision that is expensive to reverse.
- `src/pricediscovery/` — library code. `tests/` — tests, in particular for event-time alignment.

## Licence

MIT, see `LICENSE`.
