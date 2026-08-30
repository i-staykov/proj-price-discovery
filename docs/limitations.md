# Limitations

Objections in a reviewer's phrasing, with an answer or an admission that there is none. Written
before the results, so the list is part of the design rather than a defence of the outcome.

Each is marked **structural** if no ticket in this project can reduce it, or **reducible** if one
could.

## Bitcoin is not the asset that CPI is about

*A US inflation print is information about US inflation. You are measuring the price of a bearer
asset traded mostly outside the US, held largely by people with no exposure to the CPI basket. Why
should its incorporation speed tell anyone anything about how markets absorb macro news?*

No answer that rescues external validity. The result is about how fast one continuously traded venue
repriced on a scheduled macro release, and generalising it to Treasuries or equity index futures is
unsupported.

The design gains what it loses. Crypto trades continuously, so an 08:30 ET release lands in an open
market with no auction, no session boundary and no queue of overnight orders. In the assets the
release is nominally about, the same event is confounded by market structure this study would then
have to model. That is a trade, not a free choice.

**Structural.**

## The eventual move is not the release

*You define the eventual move as the return over the hour after the release. That hour contains
everything else that happened. On a quiet morning it is mostly the release; on a busy one your
denominator is noise, and you have no way to tell the two apart.*

Correct, and the price of having no consensus forecast to measure the surprise against. The model
mitigates rather than solves: the size of the move is a per-event parameter, so an event whose window
was dominated by unrelated news produces a diffuse posterior on its rate rather than a confident
wrong answer.

$m_e(H)$ cannot be decomposed into release and non-release components. Nothing in the free data
supports it.

**Structural**, given free data only.

## Conditioning on a release having moved the price

*The interesting events are the ones where the price moved. The moment you select on that, you are
choosing events using information from after the release, and your curve is a curve of the events
that happened to move.*

The objection the model is built around. The estimand is a ratio of expectations, so
$R(\tau)/R(H)$ is never formed; magnitude and rate are fitted jointly, and a release that moved
nothing contributes weak evidence about its rate rather than a divergent ratio. No event is dropped
for being uninformative.

Exclusion rules are fixed in `PREREGISTRATION.md` before any fit and concern data integrity only.

**Answered**, if the preregistered exclusions hold. A reviewer should check that the merged
preregistration predates the first estimation commit.

## One hour is a number you chose

*Nothing makes an hour the right terminal horizon. It sits in the denominator of your estimand, so
every number you report is conditional on it, and you picked it before seeing any data.*

Conceded. One hour is long enough for a macro release to be digested and short enough to limit
unrelated news, and no sharper argument is available.

Sensitivity to $H \in \{30\,\mathrm{min}, 4\,\mathrm{h}\}$ is preregistered and reported whichever
way it falls. The check is not a formality: $H$ enters $\phi$ through $1 - e^{-\lambda H}$, so it
bites hardest when the half-time is an appreciable fraction of $H$, which is the regime the study
cannot rule out in advance.

**Structural.** Any endogenous definition of the eventual move needs some horizon.

## The exponential form is assumed, not tested

*You fit one rate per event. If the price overshoots and reverts, or moves in two stages, a single
exponential describes neither and you will report a compromise number as though it were a speed.*

Conceded. $\phi_e$ is monotone in $\tau$ by construction, so the model cannot represent reversion at
all, and two panels of the #6 grid already look like overshoot.

Diagnosed from residual structure across horizons: systematic positive residuals at short $\tau$ and
negative at medium $\tau$. If the diagnostic fires it is reported as a finding about the shape of
incorporation, not repaired by refitting until the residuals look tidy.

**Reducible**, by fitting an overshoot-capable alternative and comparing.

## Everything is measured from one tick

*Your returns start at the last price before 08:30:00. That is a single trade, which sits on one side
of the spread. You have injected a common error into every horizon at once, and it is largest
relative to the signal at exactly the horizon you care most about.*

No answer, and the objection we would raise first. Bid-ask bounce at the baseline shifts the whole
curve for that event, and at $\tau = 1$ s the accumulated move may be of the order of the spread.

The per-event magnitude parameter absorbs part of it, since a constant offset resembles a slightly
different $M_e$. It does not absorb the distortion at the shortest horizons, where the offset is not
small relative to $m_e(\tau)$.

**Reducible**, by measuring the baseline as a mid price or a short pre-release average, at the cost
of an averaging window that then needs preregistering.

## One venue, one symbol

*Binance's clock is Binance's. Its matching engine timestamps need not agree with the instant BLS
published the number, and at one-second resolution that is not a rounding error. You are also
reporting a property of one exchange as though it were a property of the market.*

No answer on the clock. Binance's timestamps cannot be verified against an independent reference with
free data, and an offset of a few hundred milliseconds would distort the shortest horizons most,
which are the horizons the study is about.

A second symbol or exchange would show whether the curve is a property of the venue. It is not in the
minimum viable study.

**Structural** on the clock; **reducible** on the venue.

## The sample is small and the intervals will be wide

*212 events. Your population spread will be poorly identified, and any subgroup contrast will have
intervals wide enough to contain no effect and a large one.*

Accepted, and the reason for partial pooling rather than per-event fits. The pooled half-time should
be reasonably determined; the year and release-type contrasts are the constrained comparisons.

A wide interval reported as wide is not a failure. An interval narrowed by treating nested horizons
as independent would be.

**Structural.** The event count is fixed by how often the BLS publishes.

## FOMC is excluded, so this is a claim about 08:30 ET

*You dropped the one release type that does not arrive in the morning. Whatever you find is
conditional on that hour, and you cannot distinguish incorporation speed from morning liquidity.*

Correct. The exclusion is forced by contamination rather than chosen, since the chair's press
conference at 14:30 ET falls inside the window (ADR 0002), but the consequence stands: the primary
result describes releases at 08:30 ET.

The FOMC robustness check is informative about direction and confounded by construction.

**Reducible**, by a design that gives FOMC its own horizon and accepts non-comparability.

## Overlapping horizons

*Your one-second return is inside your one-hour return. If the likelihood treats those as independent
observations, your intervals are too narrow and your result looks sharper than it is.*

Carried explicitly: the likelihood is multivariate normal with
$\Sigma_{e,jk} = \varsigma_e^2 \min(\tau_j, \tau_k)$, not a product of independent terms. This is the
failure mode where the error presents as a better result, so it is the first thing to check in the
estimation code.

**Answered**, and worth verifying rather than believing.
