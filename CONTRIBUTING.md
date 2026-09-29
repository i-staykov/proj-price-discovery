# Contributing

## Workflow

1. Pick an issue from the board and assign yourself.
2. Branch from `main`. Name it after the issue: `12-event-calendar`.
3. Commit with the issue number in the message: `Add BLS release timestamps (#12)`.
4. Open a pull request whose body contains `Closes #12`. CI must be green.
5. Apply one review label. Follow its approval path below; do not merge draft or blocked PRs.

## Review authority

| Label | Scope | Merge condition |
| :-- | :-- | :-- |
| `review:auto` | Mechanical work fully specified by its issue | Green `just check`, resolved conversations and the required non-author approval; then squash merge without a further owner decision |
| `review:owner` | Research or policy decisions | Owner's substantive review, plus green checks and branch-protection requirements |

Always `review:owner`: preregistration and deviations, ADRs, the model or estimand, statistical
choices, gate verdicts, reported findings, standing rules and repository permissions. A mixed PR
takes the stricter label. The label never supplies permission to bypass a blocked dependency.

Proposed policy for #36: retain the current required approval. A mechanical PR's approval confirms
its scope and green checks; it need not duplicate the implementation review. GitHub disallows
self-approval, so an owner-authored PR needs another eligible maintainer. Repository auto-merge is
disabled; `review:auto` does not claim that GitHub will merge automatically. No protection settings
are changed by this document.

`main` requires one approval, green CI and resolved conversations, with no force pushes or deletion.
Do not use administrator bypass to avoid review. An instruction to open PRs does not authorise merging.

## Stop rule

If implementation needs a decision absent from its issue, open a `type:decision` issue, link it,
label the implementation PR `blocked`, and stop that work. Do not settle the choice in code.
Independent issues may continue. A stacked PR states its base and cannot merge ahead of its blockers.

## What a good issue looks like

- **The question it answers.** If you cannot phrase it as a question, the ticket is not ready.
- **An observable Definition of Done:** an artifact, measurement or passing test.
- **A milestone**, plus an `area:` label and a `type:` label where one applies.

One question per issue, at most fifteen lines. Split independent questions, not work that merely
takes longer to run. The board's Size field is retired; the owner removes it when approving #36.

## Review

Reject anything that a working researcher would not have written. Specifically:

- Comments that say what the code does rather than why it does it.
- Docstrings restating the signature; abstractions with one caller; `try/except` that hides an error.
- Prose padding: *comprehensive*, *robust*, *seamless*, *it's important to note*.
- AI attribution trailers and generated-by footers.
- Any adjective with no measurement behind it, and any point estimate with no interval.
- Figures without axis labels and units.

`CLAUDE.md` holds the full standard.

## Things not to do

- Edit the preregistration body instead of appending a dated deviation.
- Load release-day prices into a panel or fit them before Gate 2 (#51) closes. Archive hashing in
  #38 is allowed; it does not read price rows.
- Retune `target_accept_prob`, drop events or add analyses to change a result.
- Delete negative results or conceal rejected fits.
- Quote `private/` in any public artifact.
- Type a reported number into the README instead of generating it from results.
