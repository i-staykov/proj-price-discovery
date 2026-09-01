# Framings

**Chosen: fraction of the eventual move**, estimated with a Bayesian hierarchical model.
`fraction-of-move.md` states it, `notation.md` fixes the symbols, `sample.md` gives the event
counts. `model.pdf` in the repository root is the reviewer-facing model deck; source in
`docs/model/`.

It measures speed, not completeness, and requires only prices and timestamps. The alternatives below
each require something unavailable.

## Rejected: Bayesian belief updating

Treat the price as the market's posterior mean over a latent value, $P_t = \mathbb{E}[V \mid
\mathcal{F}_t]$, and measure incorporation as the decay of $\mathrm{Var}(V \mid \mathcal{F}_t)$.
This is the framing that answers how much is ever incorporated, since the variance may plateau above
zero. The estimand chosen here concerns speed, so the additional structure buys nothing, and it
costs an assumption about market behaviour that would have to be defended rather than stated.

## Rejected: mutual information

$I(R(\tau); R(H))$ normalised by $H(R(H))$ gives a curve on $[0,1]$ with an entropy interpretation
and no dependence on consensus data.

Under joint Gaussianity with correlation $\rho$,

$$I = -\tfrac{1}{2}\log\left(1 - \rho^2\right)$$

so the estimand is a monotone transform of the correlation and the exercise reduces to $R^2$. It
earns its place only under material non-Gaussian dependence, such as tail dependence or the early
move informing the magnitude but not the sign of the eventual move. Testing that is a separate study
and needs more events than a curve fit does, since sample estimators of mutual information converge
slowly. If it is revisited, the Gaussian reduction is reported first and the measured excess over it
second.

## Rejected: anything requiring consensus forecasts

The surprise is the natural measure of an event's information content and is not available free. The
eventual move substitutes for it, which is a limitation of the study rather than a footnote here;
`docs/limitations.md` (#11) carries it.

