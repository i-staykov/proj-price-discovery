# Fraction of the eventual move

Symbols in `notation.md`.

## Estimand

Write $m_e(\tau) = \mathbb{E}[R_e(\tau)]$ for the systematic component of the response. The estimand
is

$$\phi_e(\tau) = \frac{m_e(\tau)}{m_e(H)}$$

reported at the horizons in $\mathcal{T}$ with credible intervals and summarised by the population
half-time.

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

Normalising by $1 - e^{-\lambda_e H}$ rather than by the asymptote makes $\phi_e(H) = 1$ hold at $H$
rather than in the limit. The denominator is a function of a parameter, bounded in $(0,1)$, so no
observation enters it.

The free parameter is $M_e$ rather than the asymptote $A_e = M_e/(1 - e^{-\lambda_e H})$, because
$M_e$ refers to a horizon inside the data while $A_e$ extrapolates a functional form that may be
wrong.

### Observation model

The horizons are nested, so the returns are not independent. Under a random-walk background the
joint distribution over the grid is

$$\mathbf{R}_e \sim \mathcal{N}\!\left(\mathbf{m}_e,\ \Sigma_e\right),
\qquad \Sigma_{e,jk} = \varsigma_e^2 \min(\tau_j, \tau_k)$$

Variance grows with the horizon because the background accumulates. Ignoring the off-diagonal terms
would treat each horizon as fresh evidence and narrow the intervals, which is the error that
presents as a sharper result.

$\varsigma_e$ varies by event. Crypto volatility differs by an order of magnitude across the sample
period, and a shared scale would force the model to reconcile that through $\lambda_e$.

### Population level

$$\log \lambda_e \sim \mathcal{N}(\mu, \sigma^2), \qquad
\log |M_e| \sim \mathcal{N}(\mu_M, \sigma_M^2), \quad \operatorname{sign}(M_e) \text{ free}$$

Logarithms because both quantities are positive and span orders of magnitude.

$\mu$ and $\sigma$ are estimated, not supplied. $\mu$ carries the headline answer through the
population half-time; $\sigma$ sets the degree of shrinkage and answers whether a single population
speed exists.

Partial pooling is required by the sample: at $E = 214$ (`sample.md`) no pooling gives per-event
posteriors too diffuse to report, and complete pooling forecloses the release-type and year
contrasts.

The hierarchy is non-centred, $\log\lambda_e = \mu + \sigma z_e$ with $z_e \sim \mathcal{N}(0,1)$.
Events with small $M_e$ carry almost no information about their own rate, so the centred form has a
funnel geometry that Hamiltonian Monte Carlo samples badly. Divergent transitions are a failed fit,
not a diagnostic to be relaxed away.

No conditional of $\lambda_e$ has a closed form, since $\lambda_e$ enters inside the exponential, so
the joint posterior is sampled. Reported intervals are quantiles of the draws.

## Priors

In `PREREGISTRATION.md`, with the argument for each. They are fixed before any fit and not revised
afterwards, which is why they live there rather than here.

## Reported quantities

- $\phi(\tau)$ at each horizon with a 95% band. Axes: seconds since release (log scale), fraction of
  eventual move (dimensionless).
- The population half-time in seconds, with an interval.
- $\sigma$. A large $\sigma$ is a result: incorporation speed is a distribution, not a constant.
- Release-type and year contrasts on $\mu$, as group effects in the same model.

The half-time solves $\phi(\tau) = 1/2$:

$$\tau_{1/2}(\lambda) = \frac{1}{\lambda}\,\ln\frac{2}{1 + e^{-\lambda H}}$$

It tends to $\ln 2/\lambda$ as $H \to \infty$ and is shorter for finite $H$. It is computed per
posterior draw and reported as a posterior quantity, never as a transform of a point estimate.

## Validation

The model is fitted to simulated data with known $\lambda$ and must recover it before any release
data is used. This is simulation-based calibration, not estimation within the meaning of the second
standing rule, and it is what separates an unidentified parameter from a result.

Where this model breaks is `docs/limitations.md`, in a reviewer's phrasing.
