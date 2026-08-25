# Standing rules

Permanent rules about the work. Everything here applies to every ticket, every commit, every review.
If a rule stops being true, change it here in a commit rather than working around it.

## The project

A measurement study: how fast does the market incorporate new public information?

Scheduled US macro releases (CPI and Employment Situation at 08:30 ET, FOMC statements at 14:00 ET)
are the information events. They are exogenous and timestamped to the second. Prices come from
`data.binance.vision`, which is free and needs no API key; crypto trades continuously, so releases
land in open markets with no session effects to model.

The estimand is not yet decided. Choosing it is scheduled work in the Scoping milestone. Until it is
agreed and preregistered, do not write estimation code. Any design that requires paid data is out of
scope.

**This is a measurement study, not a trading strategy.** No backtest, no Sharpe ratio, no signal. A
ticket that drifts toward alpha research gets closed with the reason stated in the comment.

## Non-negotiables

1. **Every change traces to an issue.** No commit on `main` without an issue number in the message,
   no pull request without `Closes #N`. This is what makes the repository auditable.
2. **No estimation code before `PREREGISTRATION.md` is merged.** The public commit timestamp proving
   the plan predates the results is the most valuable artifact here.
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

The repository must read as though a person wrote it. This is not style fussiness: a repository that
reads as machine-generated is worth less than nothing, because it signals that the author did not
engage with their own work. Enforce it in review, without exception.

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
- Bold marks the load-bearing claim in a paragraph, not three words a line.

### In research writing

- **No adjective without a measurement behind it.** "Significantly faster" is rejected; "0.6 s
  faster, 95% CI [0.2, 1.1]" is accepted.
- Every claim either carries a number or points to the code that produces it.
- State uncertainty. A point estimate with no interval is an unfinished sentence.
- Say plainly what was not found. Hedging that conceals a null result is the worst failure here.
- Axes get labels and units. Always.

Before merging anything, ask whether a working researcher would have written that sentence. If it
reads like padding, it is padding.
