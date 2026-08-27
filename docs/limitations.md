# Limitations

Objections in a reviewer's phrasing, with our answer or an admission that we have none. Written
before the results, so that the list is part of the design rather than a defence of the outcome.

Each objection is marked **structural** if no ticket in this project can reduce it, or **reducible**
if one could.

## Bitcoin is not the asset that CPI is about

*A US inflation print is information about US inflation. You are measuring the price of a bearer
asset traded mostly outside the US, held largely by people with no exposure to the CPI basket. Why
should its incorporation speed tell anyone anything about how markets absorb macro news?*

We have no answer that rescues external validity. The result is about how fast one continuously
traded venue repriced on a scheduled macro release, and generalising it to Treasuries or equity
index futures is unsupported.

The design gains what it loses here: crypto trades continuously, so an 08:30 ET release lands in an
open market with no auction, no session boundary and no queue of overnight orders to disentangle. In
the assets the release is nominally about, the same event is confounded by market structure this
study does not have to model. That is a real trade, not a free choice.

**Structural.**

## The eventual move is not the release

*You define the eventual move as the return over the hour after the release. That hour contains
everything else that happened. On a quiet morning it is mostly the release; on a busy one your
denominator is noise, and you have no way to tell the two apart.*

Correct, and it is the price of having no consensus forecast to measure the surprise against. The
model mitigates rather than solves: the size of the move is a per-event parameter, so an event whose
window was dominated by unrelated news produces a diffuse posterior on its rate rather than a
confident wrong answer.

What we cannot do is decompose $R_e(H)$ into release and non-release components. Nothing in the free
data supports it.

**Structural**, given free data only.

## Conditioning on a release having moved the price

*The interesting events are the ones where the price moved. The moment you select on that, you are
choosing events using information from after the release, and your curve is a curve of the events
that happened to move.*

This is the objection the model was built around. The estimand is a ratio of expectations, not of
realised returns, so $R(\tau)/R(H)$ is never formed; the model fits size and rate jointly, so a
release that moved nothing contributes weak evidence about its rate rather than a divergent ratio,
and no event is dropped for being uninformative.

Exclusion rules are fixed in `PREREGISTRATION.md` before any fit and concern data integrity only.

**Answered**, if the preregistered exclusions hold. A reviewer should check that the merged
preregistration predates the first estimation commit.

## The exponential form is assumed, not tested

*You fit one rate per event. If the price overshoots and reverts, or moves in two stages, a single
exponential describes neither and you will report a compromise number as though it were a speed.*

Conceded as a real risk. It is diagnosed from residual structure across horizons: systematic
positive residuals at short $\tau$ and negative at medium $\tau$ indicate overshoot.

If the diagnostic fires, that is reported as a finding about the shape of incorporation, not
repaired by refitting until the residuals look tidy.

**Reducible**, by fitting a two-stage or overshoot-capable alternative and comparing.

## One venue, one symbol

*Binance's clock is Binance's. Its matching engine timestamps need not agree with the instant BLS
published the number, and at one-second resolution that is not a rounding error. You are also
reporting a property of one exchange as though it were a property of the market.*

No answer on the clock. We cannot verify Binance's timestamps against an independent reference with
free data, and a systematic offset of a few hundred milliseconds would distort the shortest horizons
most, which are the horizons the study is about.

Single-venue is **reducible**: a second symbol or exchange would show whether the curve is a
property of the venue. It is not in the minimum viable study.

**Structural** on the clock; **reducible** on the venue.

## The sample is small and the intervals will be wide

*214 events. Your population spread will be poorly identified, and any subgroup contrast will have
intervals wide enough to contain no effect and a large one.*

Accepted, and the reason for partial pooling rather than per-event fits. We expect the pooled
half-life to be reasonably determined and the year-over-year and release-type contrasts to be the
constrained comparisons.

A wide interval that is reported as wide is not a failure. An interval narrowed by treating
overlapping horizons as independent observations would be.

**Structural.** The event count is fixed by how often the BLS publishes.

## FOMC is excluded, so this is a claim about 08:30 ET

*You dropped the one release type that does not arrive in the morning. Whatever you find is
conditional on that hour, and you cannot distinguish incorporation speed from morning liquidity.*

Correct. FOMC was excluded because the chair's press conference at 14:30 ET falls inside the
one-hour window (ADR 0002), which is a contamination problem rather than a preference, but the
consequence stands: the primary result describes releases at 08:30 ET.

The FOMC robustness check is informative about direction but confounded by construction.

**Reducible**, by a design that gives FOMC its own horizon and accepts non-comparability.

## Overlapping horizons

*Your one-second return is inside your one-hour return. If the likelihood treats those as
independent observations, your intervals are too narrow and your result looks sharper than it is.*

Known and accounted for in the likelihood's covariance structure rather than assumed away. This is
the failure mode where the error presents as a better result, so it is the one a reviewer should
check first in the estimation code.

**Answered**, and worth verifying rather than believing.
