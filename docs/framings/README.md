# Framings

What we chose to measure, and what we did not.

**Chosen: fraction of the eventual move**, estimated with a Bayesian hierarchical model. Full
statement in `fraction-of-move.md`, symbols in `notation.md`, event counts in `sample.md`.

It measures speed, not completeness. It needs only prices and timestamps, which is the whole reason
it is viable: the alternatives below each need something we cannot get for free.

## Rejected for now: Bayesian belief updating

Posit a latent value $V$ that the release is informative about, and treat the price as the market's
posterior mean, $P_t = \mathbb{E}[V \mid \mathcal{F}_t]$. Incorporation is then the decay of
$\mathrm{Var}(V \mid \mathcal{F}_t)$, and "priced in" acquires a meaning the chosen framing cannot
express: residual uncertainty about the true value.

This is the framing that answers *how much is ever incorporated*, since the variance can plateau
above zero. We are asking how fast, so we do not need it.

It costs an assumption that the price is a conditional expectation of a well-defined latent value.
That is a real commitment about market behaviour, and defending it is a paper of its own.

## Rejected for now: mutual information

Measure the bits about the eventual move revealed by time $\tau$:

$$I\!\left(R(\tau); R(H)\right) \quad \text{normalised by } H(R(H))$$

Appealing, because it needs no consensus data and yields a curve from 0 to 1 with a genuine units
interpretation: the fraction of the eventual move's entropy resolved by $\tau$.

**It collapses.** If $(R(\tau), R(H))$ are jointly Gaussian with correlation $\rho$, then

$$I = -\tfrac{1}{2}\log\left(1 - \rho^2\right)$$

Mutual information is then a monotone function of the correlation and contains nothing that $\rho$
did not. Estimating it would be an expensive route to $R^2$.

It earns its place only if the dependence is materially non-Gaussian: tail dependence, or the early
move predicting the magnitude of the eventual move without predicting its sign. That is plausible
here and would be a genuine finding. It is also a separate study, and it needs far more events than
a curve fit does, because estimating mutual information from samples is hard.

If we return to this, the honest version reports the Gaussian reduction first and then the measured
excess over it. A reviewer who finds the collapse unmentioned discounts everything else.

## Rejected: anything requiring consensus forecasts

The surprise, the gap between the released number and what was expected, is the natural measure of
an event's information content. Consensus forecast data is not free, so the surprise is unobserved
and the eventual move stands in for it. This is a real limitation and belongs in
`docs/limitations.md`, not a footnote here.
