# Preregistration

Written before any estimation code exists and before any release-day price data has been examined
beyond the kill-check plots in #6. Deviations from this plan are logged in the deviations section
below, with the reason, rather than edited into the text above it.

## Hypothesis

Scheduled US macro releases are incorporated into the BTCUSDT price within seconds rather than
minutes.

Stated as a testable claim: **the population half-time of incorporation is under 60 seconds.** The
half-time is the $\tau$ at which half the eventual move has occurred, $\phi(\tau) = 1/2$:

$$\tau_{1/2}(\lambda) = \frac{1}{\lambda}\,\ln\frac{2}{1 + e^{-\lambda H}}$$

The claim is that the posterior median of $\tau_{1/2}(\exp(\mu))$ is below 60 s and the 95% credible
interval excludes values above it.

The direction is not predicted. The sign of the move follows the sign of the surprise and the
surprise is unobserved; the study measures speed only.

## Estimand

$\phi(\tau) = m(\tau)/m(H)$, the fraction of the eventual move realised by event time $\tau$, where
$m(\tau) = \mathbb{E}[R(\tau)]$ and $H = 1$ hour. Reported at 1 s, 10 s, 1 min, 10 min and 1 h.

Full statement in `docs/framings/fraction-of-move.md`, symbols in `docs/framings/notation.md`,
decision and rejected alternatives in `docs/adr/0002-estimand-and-primary-sample.md`.

## Sample

BTCUSDT 1-second spot klines from `data.binance.vision`.

CPI and Employment Situation releases from **2017-09-01 to 2026-07-31**, 214 events. Both boundaries
are set by data availability, not by inspection: coverage begins the month after BTCUSDT's listing
day, which is the first month with a full second-by-second record, and ends at the last complete
month in the archive. Counts by year are in `docs/framings/sample.md`.

FOMC statements are excluded from the primary sample. The chair's press conference begins at
14:30 ET, inside the one-hour window, at every meeting since 2019, so $m(H)$ would measure the
statement and the press conference jointly. FOMC is fitted separately as a robustness check and
reported as contaminated by construction.

## Exclusions

Fixed here, before the data is inspected. An event is dropped only if:

1. The daily kline archive for the release date is missing or fails checksum verification.
2. Fewer than 95% of the seconds in $[-300, +3600]$ around the release carry a trade.
3. No trade occurs in the 60 seconds before the release, so $P(0^-)$ is undefined.

No event is dropped for having a small eventual move, an unexpected sign, an implausible rate, or a
poor fit. The count of exclusions and the reason for each is reported alongside the results.

## Analysis

For each event $e$ and horizon $\tau_k$, $R_e(\tau_k) = \log P_e(\tau_k) - \log P_e(0^-)$, where
$P_e(0^-)$ is the last traded price strictly before the release instant.

$$\mathbf{R}_e \sim \mathcal{N}(\mathbf{m}_e, \Sigma_e), \qquad
\Sigma_{e,jk} = \varsigma_e^2 \min(\tau_j, \tau_k)$$

$$m_e(\tau) = M_e\,\frac{1 - e^{-\lambda_e\tau}}{1 - e^{-\lambda_e H}}$$

$$\log\lambda_e = \mu + \sigma z_e, \quad z_e \sim \mathcal{N}(0,1); \qquad
\log|M_e| \sim \mathcal{N}(\mu_M, \sigma_M^2), \ \operatorname{sign}(M_e) \text{ free}$$

Priors:

| Parameter | Prior | Reason |
| :-- | :-- | :-- |
| $\mu$ | $\mathcal{N}(-2.7,\ 1.5^2)$ | centred on a 10 s half-time, spanning 0.5 s to 200 s at two SD |
| $\sigma$ | $\mathrm{HalfNormal}(1)$ | admits $\sigma \to 0$, so homogeneity is not excluded a priori |
| $\mu_M$ | $\mathcal{N}(\log 30,\ 1^2)$ | 30 bp, order of the moves in the #6 grid |
| $\sigma_M$ | $\mathrm{HalfNormal}(1)$ | |
| $\log\varsigma_e$ | $\mathcal{N}(\nu, \omega^2)$, $\nu \sim \mathcal{N}(0, 2^2)$, $\omega \sim \mathrm{HalfNormal}(1)$ | background volatility varies by an order of magnitude across the sample |

The prior on $\mu$ is informed by the nine kill-check events in #6. This is a soft reuse of data
that also enters the sample. It is disclosed rather than avoided: the prior is deliberately wide,
and at $E = 214$ the posterior on $\mu$ is data-dominated. A sensitivity check refits with
$\mu \sim \mathcal{N}(0, 3^2)$ and reports whether the conclusion changes.

Fitted by the No-U-Turn sampler in NumPyro: 4 chains, 1000 warmup and 2000 sampling iterations each,
`target_accept_prob = 0.8`, seeded and recorded.

A fit is accepted only if $\hat{R} < 1.01$ for every parameter, bulk and tail effective sample size
exceed 400, and there are zero divergent transitions.

`target_accept_prob` is fixed here because raising it is the standard way to make divergences
disappear without addressing what caused them. Divergences are a failed fit: they indicate the
sampler could not traverse the posterior geometry, so the draws are biased. If they occur, the
response is to report them and diagnose the geometry, not to retune until they vanish.

Uncertainty is reported as 95% credible intervals, the 2.5th and 97.5th percentiles of the posterior
draws. Every reported number carries one, and derived quantities such as the half-time are computed
per draw rather than from a point estimate.

## Before the real data

Both checks run before any release-day data is loaded, and both have criteria fixed here so that
neither can be declared passed by inspection.

**Prior predictive.** Draw parameters from the priors alone and simulate returns. At least 95% of
simulated $|R(H)|$ must fall below 500 bp, the order of the largest one-hour moves in the #6 grid. A
prior that routinely generates hour-long moves larger than any observed is misspecified regardless
of how the posterior behaves.

**Recovery.** Simulate 100 datasets of 214 events each, with parameters drawn from the priors. Fit
each and record whether the 95% credible interval for the population half-time contains the value
used to generate it. Coverage must fall in [90%, 99%], the two-standard-error band around 95% at 100
replicates rounded to whole percent. Coverage below that means the intervals are too narrow and
every reported uncertainty is overstated.

If either check fails, no release data is fitted until the model is repaired and both are rerun.

## Planned robustness checks

Declared now so that none can be presented later as though it had been planned.

1. **Terminal horizon.** Refit with $H \in \{30\,\mathrm{min},\ 4\,\mathrm{h}\}$. $H$ enters $\phi$
   through $1 - e^{-\lambda H}$, so this matters most when the half-time approaches $H$.
2. **Functional form.** Fit a two-component alternative permitting overshoot and compare by expected
   log predictive density. Two panels of the #6 grid already look like overshoot.
3. **Baseline definition.** Refit with $P(0^-)$ as the mean price over the 10 seconds before
   release, in place of the last tick, to bound bid-ask bounce at the baseline.
4. **Release type.** Estimate $\mu$ separately for CPI and the Employment Situation.
5. **Time.** Estimate a linear trend in $\mu$ over the years in the sample.
6. **Prior sensitivity.** As above, the wide prior on $\mu$.
7. **FOMC.** Fitted separately, reported as contaminated.

Checks 4 and 5 are secondary. At $E = 214$ their intervals are expected to be wide, and a wide
interval will be reported as wide rather than read as a null.

## What would falsify the hypothesis

The hypothesis is falsified if the 95% credible interval for the population half-time lies entirely
above 60 seconds. It is unsupported, rather than falsified, if the interval straddles 60 seconds;
that outcome is reported as an inconclusive measurement with the interval stated, not as a positive
finding.

Two further outcomes are recorded as failures of the study rather than results:

- The residual diagnostic shows systematic overshoot, so no single rate describes the path. The
  incorporation curve would then be uninterpretable and the finding is about the shape instead.
- Sampling does not converge under the criteria above, so the posterior is not characterised.

A null or an inconclusive result is published with the same prominence as a positive one. No
outcome licenses adding an unplanned analysis to obtain a different one.

## Deviations

Each entry states what changed, when, and why.

### 2026-08-30 — primary sample is 212 events, not 214

The verified release calendar (#17, `src/pricediscovery/release_calendar.csv`, sources in ADR 0003)
holds 106 CPI and 106 Employment Situation releases over 2017-09-01 to 2026-07-31, not 107 each. The
2025 federal shutdown removed two: no CPI was released in November 2025 (the September report was
delayed to 2025-10-24) and the October 2025 Employment Situation was cancelled. Both are absent from
the calendar, not imputed (ADR 0001).

The count is a fixed input to one procedure here: the recovery check simulates 100 datasets of
**212** events each, in place of 214. Every "$E = 214$" in `docs/framings/` and `docs/limitations.md`
is now 212. The 214 in the Sample and Analysis sections above is left as written, per the rule
against editing the plan body. FOMC, a robustness input only, is **71** realised scheduled
statements against the 45 + 29 cadence estimate that was in `docs/framings/sample.md`.
