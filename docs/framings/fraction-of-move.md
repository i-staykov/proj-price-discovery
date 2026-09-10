# Fraction of the eventual move

Symbols in `notation.md`.

## Estimand

Write $m_e(\tau)$ for the expected return conditional on event $e$'s model parameters. The estimand,
for $m_e(H)\ne0$, is

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
CPI and the Employment Situation, both at 08:30 ET. The release calendar contains only the three
study events, so it does not establish isolation from releases published by other agencies.
`docs/limitations.md` carries that unresolved screen. ADR 0002 records the sample decision.

## Model

Magnitude and speed are separated so that the quantity of interest does not depend on how large the
release's effect happened to be:

$$m_e(\tau) = M_e\,\frac{1 - e^{-\lambda_e \tau}}{1 - e^{-\lambda_e H}},
\qquad
\phi_e(\tau) = \frac{1 - e^{-\lambda_e \tau}}{1 - e^{-\lambda_e H}}$$

$M_e = m_e(H)$ cancels algebraically. Small $M_e$ supplies little information about $\lambda_e$;
pooling or the prior may then dominate its posterior. At $M_e=0$ the rate is unidentified by the
event's likelihood. No event is excluded for being uninformative.

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

Variance grows with elapsed time. A diagonal covariance would incorrectly count shared increments
as independent evidence; its effect on interval width depends on the parameter and design.

$\varsigma_e$ varies by event so that changes in background volatility need not be represented as
changes in the response curve. The covariance does not model baseline noise or within-hour changes
in volatility.

### Population level

$$\log \lambda_e \sim \mathcal{N}(\mu, \sigma^2), \qquad
\log |M_e| \sim \mathcal{N}(\mu_M, \sigma_M^2), \quad \operatorname{sign}(M_e) \text{ free}$$

These are the preregistered hierarchies. The rate is positive; the magnitude's absolute value is
positive, but “sign free” does not complete its prior. Issue #31 resolves the signed prior and units
in ADR 0005; #44 will log the change before estimation. No proposal is adopted here.

$\mu$ and $\sigma$ are estimated, not supplied. $\mu$ carries the headline answer through the
population half-time; $\sigma$ sets the degree of shrinkage and answers whether a single population
speed exists.

Partial pooling allows event heterogeneity while sharing information. Neither the event count nor
the hierarchy guarantees precision; this must be measured.

The hierarchy is non-centred, $\log\lambda_e = \mu + \sigma z_e$ with $z_e \sim \mathcal{N}(0,1)$.
Weakly informed event rates can create difficult posterior geometry in the centred form.
Non-centring can help; it does not guarantee convergence. Apply the declared fit criteria.

No conditional of $\lambda_e$ has a closed form, since $\lambda_e$ enters inside the exponential, so
the joint posterior is sampled. Reported intervals are quantiles of the draws.

## Priors

In `PREREGISTRATION.md`, with the argument for each. They are fixed before any fit and not revised
afterwards, which is why they live there rather than here.

## Reported quantities

- $\phi(\tau;\exp\mu)$ at each horizon with a 95% band, not the mean curve over event rates.
  Axes: seconds since release (log scale), fraction of
  eventual move (dimensionless).
- The population median half-time in seconds, with a posterior interval.
- $\sigma$. A large $\sigma$ is a result: incorporation speed is a distribution, not a constant.
- Release-type and year contrasts on $\mu$, as group effects in the same model.

The half-time solves $\phi(\tau) = 1/2$:

$$\tau_{1/2}(\lambda) = \frac{1}{\lambda}\,\ln\frac{2}{1 + e^{-\lambda H}}$$

It tends to $\ln 2/\lambda$ as $H \to \infty$ and is shorter for finite $H$. It is computed per
posterior draw and reported as a posterior quantity, never as a transform of a point estimate.

## Validation

The preregistered recovery study measures interval coverage across simulated datasets before real
data are fitted. It is not a rank-based simulation-based calibration test, and aggregate coverage
does not establish identification for every event or parameter regime.

Where this model breaks is `docs/limitations.md`, in a reviewer's phrasing.
