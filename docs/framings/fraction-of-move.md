# Fraction of the eventual move

The chosen framing. Symbols are defined in `notation.md`.

## The estimand

Fix a terminal horizon $H$ and call $R_e(H)$ the eventual move. The **incorporation curve** is the
fraction of it realised by $\tau$:

$$\phi_e(\tau) = \frac{R_e(\tau)}{R_e(H)}$$

The study reports $\phi$ at the horizons in $\mathcal{T}$, with credible intervals, pooled across
events. A reader who wants one number gets the half-life: the seconds by which $\phi$ reaches 0.5.

Note what this does and does not claim. $\phi_e(H) = 1$ **by construction**, because $H$ defines the
destination. The framing therefore measures *how fast* the price gets where it is going and says
nothing about whether that destination is the right price. Anyone claiming completeness from this
framing has misread it.

## Why this rather than something deeper

Two other framings are sketched in `README.md`. Both need something we do not have: a measure of the
surprise, which requires consensus forecasts, or a latent value process, which requires assuming the
price is a conditional expectation and then defending that assumption.

This framing needs only prices and timestamps. Its assumptions are visible in one line, which is
what makes it a starting point rather than a compromise.

## The problem with the obvious estimator

The obvious thing to do is compute $R_e(\tau) / R_e(H)$ per event and average.

This fails, and the way it fails is instructive. $R_e(H)$ appears in a denominator, and for events
where the release moved the price very little, $R_e(H) \approx 0$. The ratio explodes. A single
event where the eventual move was 2 basis points can produce a $\phi$ of 40 and dominate the mean.

The usual fix, dropping events with small eventual moves, **conditions on the outcome**. You would
be selecting events by a quantity measured after the release, using information you would not have
had beforehand. This is the single most likely way for this study to produce a wrong answer that
looks clean, and it is a standard enough error that a reviewer will look for it.

The way out is not to form the ratio at all. Model the returns and let $\phi$ be a derived quantity.

## The model

### One event

Assume the price approaches its eventual level exponentially:

$$\mathbb{E}[R_e(\tau)] = A_e \left(1 - e^{-\lambda_e \tau}\right)$$

Two parameters with distinct jobs. $A_e$ is the **amplitude**, where the price is heading, in basis
points. $\lambda_e$ is the **rate**, how fast it gets there, in inverse seconds. Amplitude is a
nuisance parameter: it differs across events because surprises differ in size, and we do not care
about it. Rate is the object of interest.

Separating them is what avoids the division. $\phi_e(\tau) = 1 - e^{-\lambda_e \tau}$ depends on
$\lambda_e$ alone, so a small-amplitude event contributes weak evidence about $\lambda_e$ rather
than an exploding ratio. Weak evidence is handled correctly by a wide posterior; an exploding ratio
is not handled at all.

The exponential form is a choice and needs checking. It assumes monotone approach with no overshoot.
Markets do overshoot. `README.md` lists the alternatives to test as robustness, and if the residuals
show systematic structure at short $\tau$, this form is wrong and the document must say so.

### Observation model

At each observed horizon $\tau_k$,

$$R_e(\tau_k) \sim \mathcal{N}\!\left(A_e \left(1 - e^{-\lambda_e \tau_k}\right),\ \varsigma^2 \tau_k\right)$$

Variance grows with $\tau$ because returns accumulate: over a longer window, more unrelated news
arrives. Constant variance would treat a one-second return and a one-hour return as equally precise,
which is false and would make the long horizons dominate.

$\varsigma$ is the background volatility, shared across events to begin with. Whether it should vary
by event or by regime is a robustness question, not a starting assumption.

### Pooling across events

The point of the exercise. Each event's rate is drawn from a population:

$$\log \lambda_e \sim \mathcal{N}(\mu, \sigma^2)$$

The log is not cosmetic. Rates are positive and plausibly spread over orders of magnitude, from
sub-second to minutes, so a normal prior on $\lambda_e$ itself would put mass on negative rates and
would treat the difference between 0.1 and 0.2 as equal to that between 10.1 and 10.2.

This is **partial pooling**, and it is the reason to be Bayesian here rather than a preference.
Consider the alternatives.

*No pooling*, fitting each event separately, gives $E$ independent estimates each based on one
event's data. With a handful of usable horizons per event, those posteriors are so wide that the
per-event answer is worthless.

*Complete pooling*, one $\lambda$ for all events, throws away the possibility that CPI and FOMC
differ, or that speed has changed since 2017. Those are among the more interesting questions
available.

Partial pooling gives both. Each $\lambda_e$ is shrunk toward $\mu$ in proportion to how noisy that
event's data is: clean events keep their own estimate, noisy ones borrow from the population. The
amount of shrinkage is not tuned by hand, it is inferred from $\sigma$. If events genuinely differ,
$\sigma$ comes out large and shrinkage is mild. If they do not, $\sigma$ shrinks and the model
approaches complete pooling on its own.

This is the same structure as TrueSkill, where a latent per-player skill is drawn from a population
prior and updated by match outcomes, shrinkage carrying players with few games. Here the latent
quantity is a per-event speed and the observations are prices. Same object, different domain.

Amplitudes are given their own hierarchy, $\log|A_e| \sim \mathcal{N}(\mu_A, \sigma_A^2)$, with sign
free, since surprises can be positive or negative and their magnitudes also vary by orders of
magnitude.

### Priors

To be fixed in `PREREGISTRATION.md` and not adjusted afterwards. Two orientation points from the
kill-check, which found visible jumps within seconds:

$\mu$ should be centred so that half-lives of order one second to one minute are unsurprising, with
enough spread to permit an hour if the data says so. $\sigma$ needs a prior that allows near-zero,
so the model can conclude that events are homogeneous rather than being forced to find differences.
A half-normal is the standard choice.

Prior predictive checks come before any real data: simulate curves from the prior and confirm they
look like plausible price paths rather than absurd ones.

## Reported quantities

$\phi(\tau)$ at each horizon in $\mathcal{T}$, with a 95% credible band, is the headline figure.
Axes labelled: seconds since release on a log scale, fraction of eventual move, dimensionless.

The population half-life $\ln 2 / \exp(\mu)$ in seconds, with an interval, is the one-number summary.

The spread $\sigma$ answers whether events are alike. A large $\sigma$ is itself a finding: it means
there is no such thing as *the* speed of incorporation, only a distribution of them.

Group effects, once the base model works: is $\mu$ different for CPI than for FOMC, and has it
shifted over the years. These are extensions of the same model, not new studies.

## How this could be wrong

**$H$ is arbitrary.** Chosen at one hour because it is long enough for a macro release to be
digested and short enough to avoid unrelated news. If $\phi$ at fixed $\tau$ moves substantially
when $H$ is 30 minutes or 4 hours, the result depends on an arbitrary choice and the document must
report that dependence rather than pick the flattering one.

**The exponential may not fit.** If the true path overshoots and reverts, or moves in two distinct
stages, one rate cannot represent it. Detectable in the residuals, and a real finding if so.

**The eventual move absorbs everything.** $R_e(H)$ contains the release *and* whatever else happened
in that hour. On a quiet morning that is mostly the release; on a busy one it is not.

**Overlapping windows.** $R_e(1\text{s})$ is contained in $R_e(1\text{h})$, so the observations are
mechanically dependent. The model must account for this through the covariance structure, not assume
independent horizons. Getting this wrong makes intervals too narrow, which is the failure mode that
looks like success.

**One venue.** Binance's clock and matching engine need not agree with the release instant to the
second. At horizons of one second, that is not a rounding error.

Each of these belongs in `docs/limitations.md` (#11), phrased as a reviewer would phrase it.

## Validating before touching real data

The model gets fitted to **simulated** data with known $\lambda$ first, and must recover the value
that was put in. If it cannot recover a rate it generated itself, it will not recover one from
Binance either.

This is simulation-based calibration, it is standard Bayesian workflow, and it is not estimation
code within the meaning of the second standing rule, because no release data is touched. It is how
you find out that a parameter is unidentified before the identification failure gets mistaken for a
result.
