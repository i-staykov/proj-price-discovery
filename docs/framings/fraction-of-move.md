# Fraction of the eventual move

Symbols in `notation.md`.

## Estimand

Write $m_e(\tau) = \mathbb{E}[R_e(\tau)]$ for the systematic component of the response, the part
attributable to the release rather than to whatever else arrived in the window. The estimand is

$$\phi_e(\tau) = \frac{m_e(\tau)}{m_e(H)}$$

reported at the horizons in $\mathcal{T}$ with credible intervals, and summarised by the population
half-life.

It is a ratio of expectations, not of realised returns. $\mathbb{E}[R_e(\tau)/R_e(H)]$ is a
different quantity and an unusable one: the denominator is a noisy observation that approaches zero
for uninformative releases. $\phi_e$ is a deterministic function of the model parameters, so no
division by data occurs at any point.

$\phi_e(H) = 1$ by construction. The framing measures the speed of convergence to a destination it
defines, and makes no claim that the destination is the efficient price.

The estimand requires that no second scheduled information event falls inside $(0, H]$. FOMC
statements fail this: the chair's press conference begins at 14:30 ET, 30 minutes into a one-hour
window, and has followed every meeting since 2019. The primary sample is therefore CPI and the
Employment Situation, both at 08:30 ET with nothing scheduled behind them. ADR 0002 records the
decision and the rejected alternatives.

## Model

Response magnitude and speed are separated, so that the quantity of interest does not depend on how
large the release's effect happened to be:

$$m_e(\tau) = M_e\,\frac{1 - e^{-\lambda_e \tau}}{1 - e^{-\lambda_e H}},
\qquad\text{hence}\qquad
\phi_e(\tau) = \frac{1 - e^{-\lambda_e \tau}}{1 - e^{-\lambda_e H}}$$

$M_e = m_e(H)$ is the expected move at the terminal horizon and cancels algebraically, leaving
$\phi_e$ a function of $\lambda_e$ and $H$ alone. A release with a small $M_e$ therefore yields a
diffuse posterior on $\lambda_e$ rather than a divergent ratio, and no event is excluded for being
uninformative.

The denominator $1 - e^{-\lambda_e H}$ is a smooth function of a parameter, bounded in $(0,1)$, not
an observation. It is what makes $\phi_e(H) = 1$ hold exactly rather than only in the limit
$\tau \to \infty$. For fast incorporation it is numerically indistinguishable from 1: at a 10-second
half-life and $H$ = 1 hour, $\lambda_e H \approx 250$. It departs from 1 only when the half-life
approaches $H$ itself, where it reaches 1.33 at 30 minutes and 2 at an hour, so the correction
matters exactly in the regime the study cannot rule out in advance.

The parameterisation in terms of $M_e$ rather than the asymptote $A_e = M_e/(1-e^{-\lambda_e H})$ is
deliberate. $M_e$ refers to a horizon inside the data; $A_e$ is extrapolated from a functional form
that may be wrong, and is meaningless if it is.

Observation model, at each $\tau_k \in \mathcal{T}$:

$$R_e(\tau_k) \sim \mathcal{N}\!\left(m_e(\tau_k),\ \varsigma^2 \tau_k\right)$$

Variance proportional to $\tau_k$ follows from independent increments in the background process.
Homoscedastic errors would weight hour-scale noise equally with second-scale signal.

Population level:

$$\log \lambda_e \sim \mathcal{N}(\mu, \sigma^2), \qquad
\log |M_e| \sim \mathcal{N}(\mu_M, \sigma_M^2), \quad \operatorname{sign}(M_e) \text{ free}$$

Logarithms because both quantities are positive and plausibly span orders of magnitude.

$\mu$ and $\sigma$ are estimated, not supplied. $\mu$ carries the study's headline answer through
$\ln 2/\exp(\mu)$; $\sigma$ determines both the degree of shrinkage and whether a single population
speed exists at all.

Partial pooling is required by the sample: at $E \approx 214$ across the two primary release types
(`sample.md`), no pooling gives per-event posteriors too diffuse to report, and complete pooling
forecloses the release-type and year-over-year contrasts.

No conditional of $\lambda_e$ has a closed form, since $\lambda_e$ enters inside the exponential, so
the joint posterior over $(\mu, \sigma, \{\lambda_e\}, \{M_e\}, \varsigma)$ is sampled rather than
solved. Reported intervals are quantiles of the draws.

## Priors

Fixed in `PREREGISTRATION.md`, not revised afterwards.

The prior on $\mu$ is centred on a 10 s half-life ($\log \lambda = -2.7$) with scale 1.5, spanning
roughly 0.5 s to 200 s, consistent with the sub-minute reactions in #6 and permitting slower
incorporation. Using the kill-check to set this prior is a soft use of nine events to bound a belief
over 214; it is disclosed in `PREREGISTRATION.md` rather than concealed, and at this sample size the
posterior on $\mu$ is data-dominated.

The prior on $\sigma$ is half-normal, which admits $\sigma \to 0$; a prior excluding small $\sigma$
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
$H$ enters the estimand explicitly through the denominator, so this check is not cosmetic: it is
material whenever the half-life is an appreciable fraction of $H$.

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
