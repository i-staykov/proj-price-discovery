# Notation

| Symbol | Meaning |
| :-- | :-- |
| $e \in \{1,\dots,E\}$ | event index; one scheduled release |
| $t_e$ | release instant, timezone-aware UTC (#8) |
| $\tau = t - t_e$ | event time, seconds since release |
| $P_e(\tau)$ | price on event $e$'s day at event time $\tau$ |
| $R_e(\tau) = \log P_e(\tau) - \log P_e(0^-)$ | cumulative log return from the last price before release |
| $m_e(\tau) = \mathbb{E}[R_e(\tau)]$ | systematic component: the part attributable to the release |
| $H$ | terminal horizon; working value 1 hour |
| $M_e = m_e(H)$ | expected move at the terminal horizon, basis points |
| $\mathcal{T}$ | horizon grid $\{1\,\mathrm{s}, 10\,\mathrm{s}, 1\,\mathrm{min}, 10\,\mathrm{min}, 1\,\mathrm{h}\}$ |
| $\phi_e(\tau) = m_e(\tau)/m_e(H)$ | fraction of the eventual move realised by $\tau$ |
| $\lambda_e$ | incorporation rate, $\mathrm{s}^{-1}$ |
| $\tau^{1/2}_e$ | half-time: the $\tau$ at which $\phi_e(\tau) = 1/2$, seconds |
| $\mu, \sigma$ | population mean and standard deviation of $\log \lambda_e$ |
| $\varsigma_e$ | event-specific background volatility scale |

Returns are logarithmic, quoted in basis points. Times are UTC internally; ET appears only in prose
about release schedules. Intervals are 95% credible intervals.

The grid $\mathcal{T}$ is logarithmic because the kill-check (#6) found sub-minute reactions, so a
linear grid would spend most of its points after the event of interest.

Whether $P_e$ is a trade price, a mid or a kline close follows from #7's recommendation of 1-second
klines. Event-time alignment at $\tau = 0$ is the pipeline's dominant error risk. The implementation
discretises $\tau$ to the second by keying on the kline that opens at $t_e + \tau$; ADR 0004 fixes
that convention and the resulting map from the grid $\mathcal{T}$ to array indices.
