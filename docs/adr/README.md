# Architecture decision records

One file per decision that is expensive to reverse: the estimand, the data source, the event-time
alignment convention. Number them in order, `0001-short-title.md`.

Each record states the decision, what was rejected, and the measurement or argument that decided it.
Keep them short; a record nobody rereads is a record nobody writes honestly. Template:

```markdown
# 0001 Short title

Status: accepted | superseded by 0007
Date: 2026-08-25
Issue: #12

## Context
What forced a choice, and what constrained it.

## Decision
What we chose.

## Rejected
The alternatives, and the measurement or argument that ruled each one out.

## Consequences
What this makes hard later, and what would make us revisit it.
```
