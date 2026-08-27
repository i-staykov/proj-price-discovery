# Fraction of the eventual move

Symbols in `notation.md`.

## Estimand

Write $m_e(\tau) = \mathbb{E}[R_e(\tau)]$ for the systematic component of the response. The estimand
is

$$\phi_e(\tau) = \frac{m_e(\tau)}{m_e(H)}$$

reported at the horizons in $\mathcal{T}$ with credible intervals and summarised by the population
half-life.

A ratio of expectations, not of realised returns. $\mathbb{E}[R_e(\tau)/R_e(H)]$ is a different and
unusable quantity, since its denominator is an observation that approaches zero for uninformative
releases. $\phi_e$ is a function of parameters alone, so nothing divides by data.

$\phi_e(H) = 1$ by construction: the framing measures speed of convergence to a destination it
defines and makes no claim that the destination is the efficient price.

No second scheduled release may fall inside $(0, H]$. FOMC statements fail this, since the chair's
press conference begins at 14:30 ET and has followed every meeting since 2019. The primary sample is
CPI and the Employment Situation, both at 08:30 ET. ADR 0002 records the decision.

## Model

Magnitude and speed are separated so that the quantity of interest does not depend on how large the
release's effect happened to be:

$$m_e(\tau) = M_e\,\frac{1 - e^{-\lambda_e \tau}}{1 - e^{-\lambda_e H}},
\qquad
\phi_e(\tau) = \frac{1 - e^{-\lambda_e \tau}}{1 - e^{-\lambda_e H}}$$

$M_e = m_e(H)$ cancels algebraically. A release with small $M_e$ yields a diffuse posterior on
$\lambda_e$ rather than a divergent ratio, and no event is excluded for being uninformative.

The denominator is a function of a parameter, bounded in $(0,1)$, not an observation. It makes
$\phi_e(H) = 1$ exact rather than asymptotic. At a 10 s half-life and $H$ = 1 h it is 1 to machine
precision, since $\lambda_e H \approx 250$; it reaches 1.33 at a 30 min half-life and 2 at an hour.
The correction matters precisely where the study cannot assume its own answer.

$M_e$ rather than the asymptote $A_e = M_e/(1 - e^{-\lambda_e H})$ because $M_e$ refers to a horizon
inside the data, while $A_e$ is extrapolated from a functional form that may be wrong.

### Observation model

The horizons are nested, so the returns are not independent. Under a random-walk background the
joint distribution over the grid is

$$\mathbf{R}_e \sim \mathcal{N}\!\left(\mathbf{m}_e,\ \Sigma\right),
\qquad \Sigma_{jk} = \varsigma_e^2 \min(\tau_j, \tau_k)$$

Variance grows with the horizon because the background accumulates. Ignoring the off-diagonal terms
treats each horizon as fresh evidence and narrows the intervals, which is the error that presents as
a sharper result.

$\varsigma_e$ varies by event rather than being shared. Crypto volatility differs by an order of
magnitude between 2017 and 2022, and a single scale would force the model to reconcile them by
distorting $\lambda_e$.

### Population level

$$\log \lambda_e \sim \mathcal{N}(\mu, \sigma^2), \qquad
\log |M_e| \sim \mathcal{N}(\mu_M, \sigma_M^2), \quad \operatorname{sign}(M_e) \text{ free}$$

Logarithms because both quantities are positive and span orders of magnitude.

$\mu$ and $\sigma$ are estimated, not supplied. $\mu$ carries the headline answer through
$\ln 2/\exp(\mu)$; $\sigma$ sets the degree of shrinkage and answers whether a single population
speed exists.

Partial pooling is required by the sample: at $E \approx 214$ (`sample.md`) no pooling gives
per-event posteriors too diffuse to report, and complete pooling forecloses the release-type and
year contrasts.

The hierarchy is written non-centred, $\log\lambda_e = \mu + \sigma z_e$ with
$z_e \sim \mathcal{N}(0,1)$. Events with small $M_e$ carry almost no information about their own
rate, so the centred form has a funnel geometry that Hamiltonian Monte Carlo samples badly. Divergent
transitions are treated as a failed fit, not a diagnostic to be relaxed away.

No conditional of $\lambda_e$ has a closed form, since $\lambda_e$ enters inside the exponential, so
the joint posterior is sampled. Reported intervals are quantiles of the draws.

## Priors

Fixed in `PREREGISTRATION.md`, not revised afterwards.

The prior on $\mu$ is centred on a 10 s half-life ($\log\lambda = -2.7$) with scale 1.5, spanning
roughly 0.5 s to 200 s at two standard deviations. Using #6 to set it is a soft use of nine events
to bound a belief over 214; it is disclosed in `PREREGISTRATION.md`, and at this sample size the
posterior on $\mu$ is data-dominated.

The prior on $\sigma$ is half-normal, admitting $\sigma \to 0$. A prior excluding small $\sigma$
would manufacture heterogeneity.

Prior predictive checks precede any fit.

## Reported quantities

- $\phi(\tau)$ at each horizon with a 95% band. Axes: seconds since release (log scale), fraction of
  eventual move (dimensionless).
- Population half-life $\ln 2 / \exp(\mu)$ in seconds, with an interval.
- $\sigma$. A large $\sigma$ is a result: incorporation speed is a distribution, not a constant.
- Release-type and year contrasts on $\mu$, as group effects in the same model.

## Failure modes

**$H$ is a choice.** It enters the estimand through the denominator, so sensitivity to
$H \in \{30\,\mathrm{min}, 4\,\mathrm{h}\}$ is material whenever the half-life is an appreciable
fraction of $H$, not a formality. Reported either way.

**Exponential form.** $\phi_e$ is monotone in $\tau$ by construction, so overshoot and reversion, or
two-stage incorporation, cannot be represented. Two panels of the #6 grid already look like
overshoot. Diagnosed from residual structure across $\tau$; a systematic pattern is a finding about
the shape of incorporation, not a fitting problem.

**Contamination inside the window.** $H$ must contain no second scheduled release. This excludes
FOMC; the same test applies to any release type added later.

**The eventual move is not the release.** $R_e(H)$ contains all news in the window.

**A single baseline tick.** $R_e(\tau)$ is measured from $P_e(0^-)$, one price carrying bid-ask
bounce. That error is common to every horizon and is largest relative to the signal at $\tau = 1$ s,
which is the horizon the study most depends on.

**Venue clock.** Binance's timestamps need not agree with the release instant at second resolution.

These belong in `docs/limitations.md` (#11) in a reviewer's phrasing.

## Validation

The model is fitted to simulated data with known $\lambda$ and must recover it before any release
data is used. This is simulation-based calibration, not estimation within the meaning of the second
standing rule, and it is what separates an unidentified parameter from a result.
