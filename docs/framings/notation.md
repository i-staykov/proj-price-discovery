# Notation

Symbols used by every document in this directory. Nothing here is a modelling choice; it is the
vocabulary the modelling choices are written in.

## Events

An **event** is one scheduled release: a specific CPI print, Employment Situation report or FOMC
statement. Events are indexed by $e \in \{1, \dots, E\}$.

Each event has a release instant $t_e$, the moment the number became public, as a timezone-aware UTC
timestamp. How $t_e$ is determined is #8's problem, and the whole study is downstream of getting it
right.

## Prices

$P_e(t)$ is the price of the traded asset at wall-clock time $t$ on event $e$'s day. Whether that is
a trade price, a mid price or a kline close is #7's decision; the notation does not care.

Work in **event time** $\tau = t - t_e$, seconds since release. $\tau < 0$ is before the release,
$\tau = 0$ is the instant itself. Every event is aligned so that $\tau = 0$ means the same thing for
all of them, which is the single most error-prone step in the pipeline.

The **cumulative return** at horizon $\tau$ is

$$R_e(\tau) = \log P_e(\tau) - \log P_e(0^-)$$

where $P_e(0^-)$ is the last price strictly before release. Logs so that returns add across
horizons, and so that a 1% move means the same thing at any price level.

## Horizons

The horizon grid is

$$\mathcal{T} = \{1\text{ s},\ 10\text{ s},\ 1\text{ min},\ 10\text{ min},\ 1\text{ h}\}$$

roughly logarithmic, because if price discovery is fast the interesting structure is in the first
seconds, and if it is slow the interesting structure is in the first hour. A linear grid would spend
most of its points where nothing happens.

$H$ denotes the **terminal horizon**, the $\tau$ at which we declare the move complete. $H = 1$ hour
is the working value. It is a modelling choice with consequences, not a fact, and
`fraction-of-move.md` argues about it.

The **eventual move** is $R_e(H)$, and $\phi_e(\tau) = R_e(\tau) / R_e(H)$ is the fraction of it
realised by $\tau$.

## Latent quantities

$\lambda_e > 0$ is event $e$'s **incorporation rate**, in units of inverse seconds. Larger means
faster. Its interpretable transform is the **half-life**

$$\tau^{1/2}_e = \frac{\ln 2}{\lambda_e}$$

the number of seconds by which half the eventual move has occurred. Report half-lives, not rates:
seconds are a unit a reader has intuition for.

$\mu$ and $\sigma$ are the population mean and standard deviation of $\log \lambda_e$ across events.
These are what the study is ultimately about, since they describe the market rather than one
Tuesday morning in February.

## Information sets

$\mathcal{F}_t$ is everything publicly known at time $t$. It is used only in `README.md`, where the
rejected framings need it. The chosen framing never conditions on $\mathcal{F}_t$ explicitly, which
is one of the reasons it is the cheap one.

## Conventions

Returns are logarithmic and in basis points where a number is quoted. Times are UTC internally and
labelled ET only in prose about release schedules. Intervals are 95% credible intervals unless
stated, and every reported number carries one.
