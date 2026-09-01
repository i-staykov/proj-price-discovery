# 0004 Event-time alignment convention

Status: accepted
Date: 2026-08-31
Issue: #28

## Context

`align.event_window` turns a release instant and a daily 1-second kline archive into `R(tau)`,
keyed by whole seconds relative to the release. A 1-second kline with `open_time = T` covers the
half-open interval `[T, T+1s)`; its `close` field is the last trade in that interval, observed at
`T+1s`. The function keys the result on `open_time`, so `window[tau]` is the kline that opens at
`release + tau`.

`notation.md` defines `R_e(tau) = log P_e(tau) - log P_e(0^-)` with `P_e(tau)` the price *at*
event time `tau`. A kline close keyed on its open time is the price at `tau + 1s`, not `tau`, so
the dict index and the notation disagree by one second unless the convention is written down.
Estimation will index this dict with the preregistered horizon grid; an unrecorded convention is a
silent one-second error at every horizon, largest at the 1-second horizon where it doubles the
elapsed time.

## Decision

`tau` indexes the kline that **opens** at `release + tau`. The value at `tau` is that kline's
closing log return relative to `P(0^-)`, the close of the last kline that opens strictly before the
release. Consequently:

- `R(tau)` measures the move over `[release, release + (tau+1)s)`: it spans `tau + 1` seconds of
  elapsed time, not `tau`.
- `tau = 0` is the release second itself, `[release, release + 1s)`. The jump the Definition of
  Done pins lives here.
- The preregistered horizon grid `{1s, 10s, 1min, 10min, 1h}` maps to dict indices
  **`{0, 9, 59, 599, 3599}`**: horizon `k` seconds is index `k - 1`.

Downstream code reads horizons through this mapping, not by treating the key as elapsed seconds.

## Rejected

- **Renumber so `tau` carries the price at `release + tau`** (key on `close_time`, or shift the
  keys down by one). Rejected: it moves the release second to `tau = -1`, which reads wrong, and
  the kill-check (#6) already aligned on `open_time == event_utc`. Keeping the open-time key means
  `tau = 0` is the interval the release falls in, which is what the Definition of Done asks for.
  The cost is that the index is not elapsed seconds; this ADR and a test carry that.
- **Forward-fill seconds with no trade** so every `tau` in the window has a value. Rejected in the
  implementation already: a flat second and a no-trade second are different observations, and
  `tau in window` is how a caller tells them apart.

## Consequences

The grid-to-index mapping is load-bearing. `tests/test_align.py` pins the implementation; `notation.md`
points here so prose and code share one definition.
