# Fraction of the eventual move

Symbols in `notation.md`.

## Estimand

$$\phi_e(\tau) = \frac{R_e(\tau)}{R_e(H)}$$

reported at the horizons in $\mathcal{T}$ with credible intervals, and summarised by the population
half-life. $\phi_e(H) = 1$ by construction: the framing measures the speed of convergence to a
destination it defines, and makes no claim that the destination is the efficient price.

The estimand requires that no second scheduled information event falls inside $(0, H]$. FOMC
statements fail this: the chair's press conference begins at 14:30 ET, 30 minutes into a one-hour
window, and has followed every meeting since 2019. The primary sample is therefore CPI and the
Employment Situation, both at 08:30 ET with nothing scheduled behind them. ADR 0002 records the
decision and the rejected alternatives.

## Model

The ratio is never formed. $R_e(H)$ is small for uninformative releases, so a per-event ratio is
unstable, and the usual repair of dropping small-move events conditions on the outcome. Amplitude
and rate are separated instead:

$$\mathbb{E}[R_e(\tau)] = A_e\left(1 - e^{-\lambda_e \tau}\right), \qquad
\phi_e(\tau) = 1 - e^{-\lambda_e \tau}$$

so $\phi_e$ is free of $A_e$ algebraically. A low-amplitude event yields a diffuse posterior on
$\lambda_e$ rather than a divergent ratio.

Observation model, at each $\tau_k \in \mathcal{T}$:

$$R_e(\tau_k) \sim \mathcal{N}\!\left(A_e\left(1 - e^{-\lambda_e \tau_k}\right),\ \varsigma^2 \tau_k\right)$$

Variance proportional to $\tau_k$ follows from independent increments in the background process.
Homoscedastic errors would weight hour-scale noise equally with second-scale signal.

Population level:

$$\log \lambda_e \sim \mathcal{N}(\mu, \sigma^2), \qquad
\log |A_e| \sim \mathcal{N}(\mu_A, \sigma_A^2), \quad \operatorname{sign}(A_e) \text{ free}$$

Logarithms because both quantities are positive and plausibly span orders of magnitude.

Partial pooling is required by the sample: at $E \approx 214$ across the two primary release types
(`sample.md`), no pooling gives per-event posteriors too diffuse to report, and complete pooling
forecloses the release-type and year-over-year contrasts. Shrinkage is governed by $\sigma$, which
is estimated rather than fixed.

## Priors

Fixed in `PREREGISTRATION.md`, not revised afterwards.

$\mu$ is centred on a 10 s half-life ($\log \lambda = -2.7$) with scale 1.5, spanning roughly
0.5 s to 200 s, consistent with the sub-minute reactions in #6 and permitting slower incorporation.
$\sigma$ takes a half-normal prior, which admits $\sigma \to 0$; a prior excluding small $\sigma$
would manufacture heterogeneity. Prior predictive checks precede any fit.

## Reported quantities

- $\phi(\tau)$ at each horizon with a 95% band. Axes: seconds since release (log scale), fraction of
  eventual move (dimensionless).
- Population half-life $\ln 2 / \exp(\mu)$ in seconds, with an interval.
- $\sigma$. A large $\sigma$ is a result: it means incorporation speed is a distribution rather than
  a constant.
- Release-type and year contrasts on $\mu$, as group effects in the same model.

## Failure modes

**$H$ is a choice.** If $\phi(\tau)$ at fixed $\tau$ moves materially under $H \in \{30\,\mathrm{min},
4\,\mathrm{h}\}$, the result is a function of an arbitrary constant and the sensitivity is reported.

**Contamination inside the window.** $H$ must contain no second scheduled release. This is why FOMC
is excluded from the primary sample; the same test applies to any release type added later.

**Exponential form.** Overshoot and reversion, or two-stage incorporation, are not representable by
a single rate. Diagnosed from residual structure across $\tau$; a systematic pattern is a finding,
not a fitting problem.

**The eventual move is not the release.** $R_e(H)$ contains all news in the window.

**Overlapping horizons.** $R_e(\tau_k)$ is nested in $R_e(\tau_{k+1})$, so the observations are
mechanically dependent. The likelihood must carry that covariance; treating horizons as independent
narrows the intervals and the error presents as a sharper result.

**Venue clock.** Binance's timestamps need not agree with the release instant at second resolution.

These belong in `docs/limitations.md` (#11) in a reviewer's phrasing.

## Validation

The model is fitted to simulated data with known $\lambda$ and must recover it before any release
data is used. This is simulation-based calibration, not estimation within the meaning of the second
standing rule, and it is what separates an unidentified parameter from a result.
