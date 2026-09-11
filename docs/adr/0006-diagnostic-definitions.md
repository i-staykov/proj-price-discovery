# 0006 Diagnostic and robustness definitions

Status: proposed, requires owner review
Date: 2026-09-11
Issue: #43

## Context

The preregistration names an overshoot failure and seven robustness checks without defining all
their statistics or models. These choices must precede fitting. Acceptance of this ADR requires
the deviation in #44; this proposal does not amend the plan or authorise estimation.

## Residual and overshoot rule

For each posterior draw, let $L_e$ be the lower Cholesky factor of the event covariance. Define

$$u_e=\operatorname{sign}(M_e)L_e^{-1}(\mathbf R_e-\mathbf m_e),\qquad
\bar u_k=E^{-1}\sum_e u_{ek}.$$

At $M_e=0$, define the sign multiplier as zero. No event is removed. Cholesky standardisation gives
unitless residuals for successive intervals $(\tau_{k-1},\tau_k]$, with $\tau_0=0$, rather than
counting shared increments repeatedly. Direction alignment prevents positive and negative events
from cancelling. Dividing by $M_e$ is rejected: near-zero magnitudes recreate an unstable ratio.

Let $q_p(\bar u_k)$ be the posterior $p$-quantile. On the primary grid, the overshoot rule fires iff

$$[q_{0.025}(\bar u_{10})>0\ \lor\ q_{0.025}(\bar u_{60})>0]
\quad\land\quad q_{0.975}(\bar u_{600})<0.$$

Subscripts here name interval endpoints in seconds, not array indices. Positive early residual
increments followed by negative increments indicate excess early movement followed by reversion.
These are posterior intervals for fitted residual means, not predictive intervals for new events.
Posterior-dependent sign alignment can affect weak events; #53 must test the rule on one-rate and
overshoot simulations before interpreting it on prices. The rule detects this pattern, not every
departure from the model.

## Check 2: one reversion component

With $f_e(t)=(1-e^{-\lambda_e t})/(1-e^{-\lambda_e H})$, use

$$m_e^{(2)}(t)=M_e[f_e(t)+a_e b_e(t)],\qquad
b_e(t)=f_e(t)\frac{e^{-\kappa_e t}-e^{-\kappa_e H}}{1-e^{-\kappa_e H}}.$$

Both $b_e(0)$ and $b_e(H)$ are zero. Thus the terminal magnitude remains $M_e$, and $a_e=0$
recovers the one-rate curve exactly. Positive amplitude permits overshoot; negative amplitude
permits delayed movement. Use the same background likelihood and the ADR 0005 base priors.

| Additional parameter | Prior or non-centred definition |
| :-- | :-- |
| `amplitude_location` | $\mathcal N(0,0.5^2)$ |
| `amplitude_scale` | $\mathrm{HalfNormal}(0.25)$ |
| $z_{a,e}$ | $\mathcal N(0,1)$ |
| $a_e$ | `amplitude_location` + `amplitude_scale` $z_{a,e}$ |
| $\log\kappa_e$ | $\mathcal N(\log(1/120),1^2)$, rates in $\mathrm{s}^{-1}$ |

Amplitude is a fraction of terminal magnitude, so its prior does not depend on return units.
Its location is a named population parameter that simulation can pin. The reversion time prior
centres on 120 seconds and permits a factor $e$ either side at one standard deviation. These are
design priors, not estimates from release prices. A second unrestricted terminal magnitude is
rejected because it would change the definition of $M_e$.

Report amplitude location and predictive comparison, not a unique half-time for a nonmonotone path.

### Predictive comparison

Attempt PSIS-LOO with each event vector as one observation. Use a Pareto threshold $k=0.7$.
If either model has any $k>0.7$, any non-finite $k$, or a failed PSIS calculation, use 10-fold
cross-validation for both. Do not compare different estimators across the two models. For a quick
run, $K=\min(10,E)$. Order events by `(date, release_type)` and assign rank modulo $K$ to folds.

For each held-out event $e$ and training-posterior draw $s$, draw $J=1024$ fresh event-parameter
vectors $\theta_e^{(s,j)}$ from the population distribution conditional on that draw. Include all
event effects and any declared covariates. Never reuse that event's full-data parameter draws.
Compute

$$\ell_{se}=\log\left[J^{-1}\sum_{j=1}^J
p(\mathbf R_e\mid\theta_e^{(s,j)})\right],\qquad
\ell_e=\log\left[S^{-1}\sum_{s=1}^S e^{\ell_{se}}\right].$$

Use log-sum-exp for both averages. `model.log_predictive` returns the $S\times E_{heldout}$ array
$\ell_{se}$; the runner performs the outer average. Fix the integration seeds alongside fold-fit
seeds. The inner count limits computation while sampling new event effects rather than setting
them to their population means. Split the 1024 inner draws into four batches of 256 and recompute
each total ELPD and their difference by batch, keeping posterior draws fixed. Report the sample SD
of each four-batch statistic divided by $\sqrt4$ under `extra.integration_mcse`, as an approximate
integration-only standard error. It excludes posterior-chain error and is distinct from the
between-event standard error below.

ELPD is $\sum_e\ell_e$. For a difference use $d_e=\ell_{e,2}-\ell_{e,1}$ and
$\mathrm{SE}(\sum_e d_e)=\sqrt{E\operatorname{Var}_{e,ddof=1}(d_e)}$; use the same event-wise
formula for each model's total. Report estimate plus or minus $2\mathrm{SE}$, labelled as such,
not as posterior credible intervals. Report every fold's acceptance verdict; a failed fold makes
the comparison unavailable rather than licensing a replacement fit.

## Checks 1, 3, 4 and 5

| Check | Definition | Reason |
| :-- | :-- | :-- |
| Terminal horizon | At 1800 s: $(1,10,60,600,1800)$; at 14400 s: $(1,10,60,600,3600,14400)$ | Preserve the early grid; retain the primary one-hour observation in the longer arm |
| `mean10` baseline | Arithmetic mean of traded closes at indices $-10$ to $-1$; if none, use the primary last traded pre-release close and record fallback | Keep the same eligible events; no new exclusion based on the baseline arm |
| Release type | $\log\lambda_e=\mu+\delta I(e=\mathrm{EmploymentSituation})+\sigma z_e$, $\delta\sim\mathcal N(0,1^2)$ | CPI is the reference; one prior SD permits a factor $e$ in the median rate |
| Time | $\log\lambda_e=\mu+\beta x_e+\sigma z_e$, $\beta\sim\mathcal N(0,0.15^2)$ | One prior SD permits a factor $e^{0.15}$ in rate per year |

For the trend, $x_e$ is elapsed days from the midpoint of `SAMPLE_START` and `SAMPLE_END`, divided
by 365.2425. The midpoint is fixed from calendar boundaries, not recomputed after exclusions.
Type and trend are separate fits; no interaction or combined model is added. The four-hour arm
is labelled contaminated by construction because it spans later scheduled releases.

## Missing grid seconds

Keep `align.event_window` sparse. To read horizon $t$, use its value at $t-1$ if present, otherwise
the latest present index less than $t-1$. Retained events have a traded pre-release baseline.
Record the number of carried grid reads per event; coverage and exclusions count actual traded
seconds, never carried values. This extends the baseline's last-trade convention without altering
ADR 0004's raw alignment representation.

Dropping missing cells is rejected here because it removes exactly the short-horizon observations
whose availability the sensitivity analysis needs to expose. Carrying a close is a measurement
convention, not evidence of a trade at the horizon; it does not make the Brownian covariance exact
for stale prices. The carried-read count must accompany the result.

## Shift from primary

`shift_from_primary_s` is the refit's posterior median half-time minus the primary's posterior
median half-time. Its `lo` and `hi` fields are null; each fit retains its own 95% interval.
Independent subtraction of two posterior draw sets is rejected because the fits share data and
that interval would not represent a jointly modelled contrast. This descriptive difference cannot
support a significance claim or replace the primary verdict.

## Consequences

This ADR specifies checks, not evidence that they pass. #44 logs the definitions and their effect
on interpretation. Gate 1 reviews the specification; #53 checks residual behaviour and #58 checks
predictive separation on simulations. Failure is reported and diagnosed, not repaired by changing
thresholds or seeds after inspecting results.
