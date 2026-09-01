# Copilot instructions

Read `CLAUDE.md` first; it holds the standing rules for this repository. The writing standard below
is repeated here because it is what gets violated most often by generated code.

This is a measurement study of how fast prices incorporate scheduled macro releases. It is not a
trading strategy. Do not propose backtests, Sharpe ratios or signals.

The estimand is fixed in ADR 0002 and the analysis is preregistered. Estimation must follow
`PREREGISTRATION.md`; changes are logged as deviations rather than edited into the plan.

## Code

- Comments explain why, never what.
- No docstring that restates the signature.
- No abstraction without a second caller.
- No `try/except` that swallows errors. Let failures be loud.
- No defensive validation of inputs that cannot occur.
- Names carry information. `df2`, `data_processed` and `helper` are rejected.

## Prose, including commit messages and issue text

- Cut phrases that survive their own deletion: *it's important to note*, *comprehensive*, *robust*,
  *seamless*, *leverage*, *delve into*.
- No sentence that restates its heading. No summary that adds nothing.
- Full sentences where there is reasoning; bullets only for genuine lists.
- No emoji in code, commit messages or ADRs.
- No AI attribution trailers or generated-by footers.
- No adjective without a measurement behind it. State uncertainty as an interval.
- Axes get labels and units.

## Length

Assume the reader stops after fifteen lines, because they do. An issue is at most fifteen lines; a
pull request body at most ten. Say a thing once: an introduction and a summary that both state it
mean the reader skims both. Given two drafts with the same content, the shorter is correct.

Derivations are exempt. Length is a fault only when it is padding.

## Register

Everything committed is production. No teaching, toy examples, analogies or "recall that". Justify
a choice; do not explain the concept behind it. `model.pdf` is a concise reviewer-facing exception.

## Commits

Every commit references an issue number. Every pull request body contains `Closes #N`.
