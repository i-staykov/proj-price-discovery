# 0002 Estimand and primary sample

Status: accepted
Date: 2026-08-25
Issue: #9

## Context

The kill-check (#6) established that BTCUSDT reacts to CPI releases in 9 of 9 dates tested, median
jump ratio 5.6x against the prior weekday at the same clock time. What to measure was left open.

Three framings were compared in `docs/framings/README.md`. Two require data or assumptions the
project does not have: consensus forecasts are not free, so the surprise is unobservable, and the
belief-updating framing requires treating the price as a conditional expectation of a latent value.

## Decision

The estimand is the incorporation curve $\phi(\tau) = m(\tau)/m(H)$, where $m(\tau)$ is the expected
return at event time $\tau$: the fraction of the eventual move realised by $\tau$, reported at 1 s,
10 s, 1 min, 10 min and 1 h with 95% credible intervals, and summarised by the population half-time,
the $\tau$ at which $\phi(\tau) = 1/2$.

It is a ratio of expectations rather than of realised returns, so that no division by an observation
occurs anywhere.

It is estimated by the hierarchical model in `docs/framings/fraction-of-move.md`, which separates the
magnitude of the response from its speed so the ratio is never formed and small-move events are not
excluded.

$H = 1$ hour. The primary sample is CPI and the Employment Situation: 214 events, 2017-09 to 2026-07.

## Rejected

**Mutual information.** Under joint Gaussianity it reduces to a monotone transform of the
correlation, so the estimand would be $R^2$ obtained expensively. Worth returning to only if the
dependence is materially non-Gaussian, and testing that needs more events than a curve fit does.

**Belief updating.** Answers how much is ever incorporated rather than how fast. The question here is
speed, so the extra assumption buys nothing.

**Conditioning on a large eventual move.** The obvious repair for an unstable ratio, and it selects
on the outcome. Avoided structurally by not forming the ratio.

**FOMC in the primary sample.** The statement is released at 14:00 ET and the chair's press
conference begins at 14:30, inside the one-hour window, at every meeting since 2019. $m(H)$ would
then measure the statement and the press conference jointly, and the press conference frequently
moves the price more. Two repairs were also rejected: a shorter $H$ for FOMC alone, which makes the
release types non-comparable and puts a free parameter where the contamination is; and accepting the
contamination, which redefines the estimand for a fifth of the events without saying so. FOMC is
retained as a robustness check, where the comparison against CPI is informative precisely because
the window is contaminated.

## Consequences

The study measures speed of convergence to an endogenously defined destination. It cannot claim the
destination is the efficient price, and it cannot report how much information is ever incorporated.

$H$ enters the estimand through $1 - e^{-\lambda H}$, so every reported figure is conditional on it.
One hour is defensible within an order of magnitude and no further: long enough for a release to be
digested, short enough to limit unrelated news. Sensitivity to $H \in \{30\,\mathrm{min},
4\,\mathrm{h}\}$ is preregistered rather than performed after the fact, and matters most when the
half-time is an appreciable fraction of $H$.

Excluding FOMC costs 45 events and removes the one release type not timed at 08:30 ET, so any
finding is conditional on the morning. `docs/limitations.md` carries this.

Adding a release type later requires checking that no second scheduled release falls inside $(0, H]$.
