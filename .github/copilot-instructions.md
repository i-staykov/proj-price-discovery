# Copilot instructions

Read `CLAUDE.md` first; it holds the standing rules for this repository. The writing standard below
is repeated here because it is what gets violated most often by generated code.

This is a measurement study of how fast prices incorporate scheduled macro releases. It is not a
trading strategy. Do not propose backtests, Sharpe ratios or signals.

The estimand is undecided and no estimation code may be written before `PREREGISTRATION.md` is
merged. If asked for estimation code before then, say so instead of writing it.

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
- No adjective without a measurement behind it. State uncertainty as an interval.
- Axes get labels and units.

## Commits

Every commit references an issue number. Every pull request body contains `Closes #N`.
