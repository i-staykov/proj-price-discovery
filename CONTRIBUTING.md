# Contributing

Two people work on this repository. The process below exists to keep attribution and provenance
clean, not to add ceremony.

## Workflow

1. Pick an issue from the board and assign yourself, so the other person does not start the same
   work.
2. Branch from `main`. Name it after the issue: `12-event-calendar`.
3. Commit with the issue number in the message: `Add BLS release timestamps (#12)`.
4. Open a pull request whose body contains `Closes #12`. CI must be green.
5. The other brother reviews. Review enforces the writing standard below as much as the code.

Every commit on `main` references an issue. If you find yourself writing code with no ticket, stop
and open the ticket first; it usually turns out the scope was unclear.

## What a good issue looks like

The template asks for three things and they all matter:

- **The question it answers.** If you cannot phrase it as a question, the ticket is not ready.
- **A Definition of Done that is an observable artifact** — a file at a stated path, a figure, a
  passing test. "Investigate the calendar" is not done-able. "`data/calendar.csv` exists with one
  row per release and a test asserting all timestamps are timezone-aware UTC" is.
- **A milestone**, plus an `area:` label and a `type:` label where one applies.

Size is a Fibonacci number on the board: 1 is an hour or two, 2 is half an evening, 3 is a full
evening. **3 is the ceiling.** A 5 or an 8 is not an estimate, it is a signal that the ticket has not
been thought through; split it and say so in the parent.

## Review

Reject anything that a working researcher would not have written. Specifically:

- Comments that say what the code does rather than why it does it.
- Docstrings restating the signature; abstractions with one caller; `try/except` that hides an error.
- Prose padding: *comprehensive*, *robust*, *seamless*, *it's important to note*.
- Any adjective with no measurement behind it, and any point estimate with no interval.
- Figures without axis labels and units.

`CLAUDE.md` holds the full standard. It is worth rereading before a review rather than after one.

## Things not to do

Do not write estimation code before `PREREGISTRATION.md` is merged. Do not quietly edit
`PREREGISTRATION.md` after the fact; log the deviation and why. Do not delete a negative result. Do
not put anything from `private/` into a public file, an issue or a commit message.
