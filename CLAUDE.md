# Standing rules

Permanent rules about the work. Everything here applies to every ticket, every commit, every review.
If a rule stops being true, change it here in a commit rather than working around it.

## The project

A measurement study: how fast does the market incorporate new public information?

The primary events are CPI and Employment Situation releases at 08:30 ET. FOMC statements at
14:00 ET are a robustness sample because the chair's 14:30 press conference contaminates the
one-hour window. Prices come from `data.binance.vision`; crypto trades continuously, so releases
land in an open market with no session boundary to model.

ADR 0002 fixes the estimand and `PREREGISTRATION.md` fixes the analysis. Estimation follows that
plan. Any change is logged as a deviation, and any design requiring paid data is out of scope.

**This is a measurement study, not a trading strategy.** No backtest, no Sharpe ratio, no signal. A
ticket that drifts toward alpha research gets closed with the reason stated in the comment.

## Non-negotiables

1. **Every change traces to an issue.** No commit on `main` without an issue number in the message,
   no pull request without `Closes #N`. This is what makes the repository auditable.
2. **Estimation follows the merged `PREREGISTRATION.md`.** Its public commit timestamp proves the
  plan predates the results; changes are logged as deviations rather than edited into the plan.
3. **A null result is a success.** Plan for it. Never delete a negative result; record it alongside
   the measurement that produced it.
4. **Every number in the README is generated, never typed.** `just results` regenerates all figures
   and reported numbers from raw data.
5. **Nothing personal in the public repository.** `private/` is gitignored and stays that way.
6. **Size discipline.** No issue larger than one evening. Split anything bigger.

## Decisions

Any choice that is expensive to reverse, such as the estimand, the data source, or the alignment
convention, gets a short ADR in `docs/adr/` and a `type:decision` issue recording what was chosen,
what was rejected, and the measurement or argument that decided it.

If a preregistered choice is later changed, log the deviation and the reason. Do not silently edit
`PREREGISTRATION.md`.

## Writing standard

Write for a working researcher. Remove generated filler before review.

### In code

- Comments explain why, never what. `# increment the counter` above `i += 1` is deleted on sight.
- No docstring that restates the signature. If the name and types make it obvious, write nothing.
- No abstraction without a second caller. No wrapper that forwards to one function.
- No `try/except` that swallows an error to keep things robust. Let it fail loudly.
- No defensive validation of inputs that cannot occur.
- Names carry information. `df2`, `data_processed` and `helper` are rejected.

### In prose

- Cut every phrase that survives its own deletion: *it's important to note*, *comprehensive*,
  *robust*, *seamless*, *leverage*, *delve into*, *in the world of*.
- No sentence that restates the heading above it.
- No summary section that adds nothing to what preceded it.
- Full sentences where there is reasoning. Bullets only for genuine lists.
- No emoji in code, commit messages or ADRs. The README status line may use one marker, no more.
- No AI attribution trailers or generated-by footers. The human author owns the change.
- Bold marks the load-bearing claim in a paragraph, not three words a line.

### Length

- An issue is at most fifteen lines: a question, a Definition of Done, and anything a reader could
  not work out alone. If it needs more, it is two issues.
- A pull request body is at most ten lines.
- A document says a thing once. Saying it in an introduction and again in a summary is saying it
  zero times, because the reader learns to skim both.
- Given two drafts with the same content, the shorter one is correct.

The exception is derivation. A modelling argument may run long, because each line does work. Length
is a fault only when it is padding.

### Register

**Everything committed here is production.** Write for a competent reviewer.

No teaching in the repository: no toy examples, analogies or "recall that". State the model, the
assumption and what breaks it. Author notes stay outside the repository. `model.pdf` is a concise
reviewer-facing exception and must agree with the model documents.

### In research writing

- **No adjective without a measurement behind it.** "Significantly faster" is rejected; "0.6 s
  faster, 95% CI [0.2, 1.1]" is accepted.
- Every claim either carries a number or points to the code that produces it.
- State uncertainty. A point estimate with no interval is an unfinished sentence.
- Say plainly what was not found. Hedging that conceals a null result is the worst failure here.
- Axes get labels and units. Always.

If a working researcher would not have written it, cut it.
